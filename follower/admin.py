from django.contrib import admin
from .models import *
# Register your models here.

class FollowListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = FollowList

class FollowRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'reciever']
    list_display = ['sender', 'reciever']
    search_fields = ['sender__username', 'reciever__username']

    class Meta:
        model = FollowRequest

admin.site.register(FollowList, FollowListAdmin)
admin.site.register(FollowRequest, FollowRequestAdmin)
admin.site.register(ChatRoom)
admin.site.register(Message)
