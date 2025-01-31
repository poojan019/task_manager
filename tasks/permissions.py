from rest_framework import permissions

class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == ['MANAGER', 'ADMIN']
    
class IsTaskAssigneeOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user or request.user.role == 'ADMIN'