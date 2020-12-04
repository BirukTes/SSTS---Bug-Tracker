from django.contrib import admin
from .models import *

admin.site.register(BugTicket)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'bugTicket')

admin.site.register(Comment, CommentAdmin)