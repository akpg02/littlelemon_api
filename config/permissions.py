from rest_framework import permissions

class MenuItemsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.groups.filter(name='manager').exists() or request.user.is_staff)

class ManageGroupPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.groups.filter(name='manager').exists() or request.user.is_staff)

class CartPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)
    
class OrderPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)
    
class CategoryPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.is_staff)
