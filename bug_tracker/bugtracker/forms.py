from django.forms import ModelForm
from .models import BugTicket, Comment


class BugTicketForm(ModelForm):
    class Meta:
        model = BugTicket
        fields = ['description', 'type', 'status', 'priority', 'responsibleTeamMember', 'finderUserName']

    def __init__(self, *args, **kwargs):
        super(BugTicketForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "Enter ticket description here", 'rows': '5'})
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['responsibleTeamMember'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-control'})
        self.fields['priority'].widget.attrs.update({'class': 'form-control'})


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'bugTicket', 'user']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "Enter comment here", 'rows': '5'})
