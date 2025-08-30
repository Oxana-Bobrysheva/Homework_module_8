from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()
