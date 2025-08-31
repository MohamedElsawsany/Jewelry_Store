from rest_framework.permissions import BasePermission

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['Admin', 'Manager']

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'

class SameBranchPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'branch_id'):
            return request.user.branch_id == obj.branch_id
        return True