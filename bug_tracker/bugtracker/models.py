from django.db import models
from django.contrib.auth.models import User


# class user(object):
#     """
#     docstring
#     """
#     pass

# Bug Ticket
class BugTicket(models.Model):
    """
    Bug Ticket
    """
    TYPE = (('Development', 'Development'),
			('Testing', 'Testing'),
			('Production', 'Production'),
			)
    STATUS = (('Open', 'Open'),
			('Resolved', 'Resolved'),
			('Closed', 'Closed'),
			)
    PRIORITY = (('High', 'High'),
			('Medium', 'Medium'),
			('Low', 'Low'),
			)
    
    description = models.TextField(null=False)
    dateTime = models.DateTimeField(auto_now_add=True, null=False)
    type = models.CharField(max_length=30, null=False, choices=TYPE)
    status = models.CharField(max_length=30, null=False, choices=STATUS, default='Open')
    priority = models.CharField(max_length=30, null=False, choices=PRIORITY, default='Medium')
    responsibleTeamMember = models.ForeignKey(User, on_delete=models.SET('Deleted User'), db_constraint=False, related_name='reponsibleUser', null=False)
    finderUserName = models.ForeignKey(User, on_delete=models.SET('Deleted User'), db_constraint=False, related_name='createdBy', null=False)

    def __str__(self):
        return self.description


class Comment(models.Model):
    """
    Comment
    """
    comment = models.TextField(null=False)
    dateTime = models.DateTimeField(auto_now_add=True, null=False)
    bugTicket = models.ForeignKey(BugTicket, related_name='comments', on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.SET('Deleted User'), db_constraint=False, null=False)

    def __str__(self): 
        return self.comment