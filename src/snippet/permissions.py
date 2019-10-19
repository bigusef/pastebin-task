from rest_framework.permissions import BasePermission


class IsOwnedPastes(BasePermission):
    """
    custome permission class make sure that this is the owner of object
    this object must have author attribute
    """
    def has_object_permission(self, request, view, obj) -> bool:
        """
        check based on instance
        """
        return True if request.user.profile == obj.author else False


class IsOwnedOrSharedPastes(BasePermission):
    """
    custome permission class make sure that this is the owner of object
    or he on allowed user relation
    this object must have author attribute
    thi object must have many to many relation with user profile
    """
    def has_object_permission(self, request, view, obj):
        """
        check based on instance
        """
        current_user = request.user.profile
        if current_user == obj.author or current_user in obj.allowed_user.all():
            return True
        else:
            return False
