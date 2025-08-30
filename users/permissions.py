from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()


class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ админам и модераторам
        if request.user.is_staff or request.user.groups.filter(name='moderators').exists():
            return True
        # Разрешаем доступ владельцу объекта
        return obj.owner == request.user