from django.shortcuts import redirect, render, get_object_or_404

from django.http import HttpResponse
from .forms import *
from .decorators import unauthenticated_user, allowed_users

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string


# ------------------- (DASHBOARD AND CREATION OF TICKET) -------------------
@login_required(login_url='bugtracker:login')
@allowed_users(allowed_roles=['Developer', 'Tester', 'Client'])
def main(request):
    # print(request)
    ticketList = BugTicket.objects.order_by('-dateTime')

    if request.method == 'POST':
        post = request.POST.copy()
        post['status'] = 'Open'
        post['finderUserName'] = request.user.id
        request.POST = post
        form = BugTicketForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('ok', status=200)
        else:
            return HttpResponse('error', status=500)
    elif request.is_ajax():
        context = {'ticket_list': ticketList}
        html = render_to_string('partials/ticketList.html', context)
        return HttpResponse(html)
    else:
        action = 'create'
        if str(request.user.groups.all()[0]) != 'Client':
            form = BugTicketForm()
            context = {'action': action, 'form': form,
                       'ticketList': ticketList}
        else:
            context = {'action': action, 'ticketList': ticketList}

        return render(request, 'bugtracker/main.html', context)


# ------------------- (LOGIN) -------------------
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        usernameName = request.POST.get('userName')
        userpassword = request.POST.get('userPassword')

        user = authenticate(
            request, username=usernameName, password=userpassword)

        if user is not None:
            login(request, user)
            return redirect('bugtracker:main')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'bugtracker/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('bugtracker:login')


# ------------------- (VIEW TICKET) -------------------
@login_required(login_url='bugtracker:login')
@allowed_users(allowed_roles=['Developer', 'Tester', 'Client'])
def viewTicket(request, ticket_id):
    ticket = get_object_or_404(BugTicket, pk=ticket_id)

    allowed_user = (request.user == ticket.finderUserName) or (
        request.user.groups.all()[0] == 'Developer')

    # if ticket is not None:
    comments = ticket.comments.order_by('-dateTime')
    if ticket.status != 'Closed':
        form = CommentForm()
        context = {'ticket': ticket, 'form': form,
                   'comments': comments, 'allowed_user': allowed_user}
    else:
        context = {'ticket': ticket, 'comments': comments,
                   'allowed_user': allowed_user}

    # For csrf token to work the 'request' must be provided
    html = render_to_string('bugtracker/ticketView.html',
                            context=context, request=request)
    return HttpResponse(html)


# ------------------- (UPDATE TICKET) -------------------
@login_required(login_url='bugtracker:login')
@allowed_users(allowed_roles=['Developer', 'Tester'])
def updateTicket(request, ticket_id):
    action = 'update'
    ticket = BugTicket.objects.get(id=ticket_id)
    form = BugTicketForm(instance=ticket)

    if request.method == 'POST':
        print(request.POST)
        post = request.POST.copy()
        post['finderUserName'] = ticket.finderUserName.id
        request.POST = post
        form = BugTicketForm(request.POST, instance=ticket)
        print(form)
        if form.is_valid():
            form.save()
            return HttpResponse('ok', status=200)

    context = {'action': action, 'formData': form}
    html = render_to_string('partials/addTicketForm.html',
                            context=context, request=request)
    return HttpResponse(html)


# -------------------(DELETE TICKET) -------------------
@login_required(login_url='bugtracker:login')
@allowed_users(allowed_roles=['Developer', 'Tester'])
def deleteTicket(request, ticket_id):
    ticket = BugTicket.objects.get(id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return HttpResponse('ok', status=200)

    html = render_to_string('partials/delete_csrf.html', request=request)
    return HttpResponse(html)


# ------------------- (ADD COMMENT) -------------------
@login_required(login_url='bugtracker:login')
@allowed_users(allowed_roles=['Developer', 'Tester', 'Client'])
def addComment(request):
    if request.method == 'POST':
        post = request.POST.copy()
        post['user'] = request.user.id
        request.POST = post
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save()
            context = {'comments': [comment]}
            html = render_to_string(
                'partials/commentTemplate.html', context=context)
            return HttpResponse(html, status=200)
        else:
            return HttpResponse('error', status=500)
