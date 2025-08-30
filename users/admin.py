from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone', 'city', 'is_staff', 'is_moderator')
    list_filter = ('is_staff', 'groups')

    def is_moderator(self, obj):
        return obj.groups.filter(name='moderators').exists()

    is_moderator.boolean = True
    is_moderator.short_description = 'Модератор'