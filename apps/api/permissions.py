from rest_framework import permissions

class IsOwnerAndCreatedStatus(permissions.BasePermission):
    """
    Custom permission to allow only the owner of the order to edit it if the status is 'CREATED'. Order Class
    """
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user and obj.status == 'CREATED'
