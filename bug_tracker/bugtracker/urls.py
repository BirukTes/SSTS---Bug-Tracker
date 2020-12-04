from django.urls import path
 
from . import views

app_name = 'bugtracker'
urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    #------------ (VIEW URLS) ------------
    path('<int:ticket_id>/', views.viewTicket, name='viewTicket'),
    
    #------------ (UPDATE URLS) ------------
    path('updateTicket/<int:ticket_id>/', views.updateTicket, name='updateTicket'),

    #------------ (UPDATE URLS) ------------
    path('deleteTicket/<int:ticket_id>/', views.deleteTicket, name="deleteTicket"),

    #------------ (CREATE URLS) ------------
    path('addComment/', views.addComment, name='addComment'),
    
] 