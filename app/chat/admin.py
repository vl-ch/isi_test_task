from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Thread, Message


admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_staff', )

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated', )
    ordering = ('-created', )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'thread', 'created', 'is_read', )
    ordering = ('thread', '-created', )
    search_fields = ('thread__id', 'sender__username')