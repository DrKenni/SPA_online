from rest_framework.permissions import BasePermission


class IsOwnerOrModer(BasePermission):
    message = 'Вы не являетесь владельцем или модератором!'

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object().owner


class IsModerator(BasePermission):
    message = 'У вас нет прав модератора!'

    def has_permission(self, request, view):
        if request.user.role == 'moderator':
            return True
        return False


class IsOwner(BasePermission):
    message = 'У вас нет прав владельца!'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class NotModer(BasePermission):
    message = 'У вас нет прав создателя!'

    def has_permission(self, request, view):
        return not request.user.is_staff or request.user.is_superuser
