from rest_framework.permissions import BasePermission


class IsOwnedPastes(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True if request.user.profile == obj.author else False


class IsOwnedOrSharedPastes(BasePermission):
    def has_object_permission(self, request, view, obj):
        current_user = request.user.profile
        if current_user == obj.author or current_user in obj.allowed_user.all():
            return True
        else:
            return False
