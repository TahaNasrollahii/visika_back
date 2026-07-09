from rest_framework import permissions

class IsCustomer(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_auth = super().has_permission(request, view)
        if not is_auth:
            return False
        return request.user.role == request.user.RoleChoices.CUSTOMER

class IsVendor(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_auth = super().has_permission(request, view)
        if not is_auth:
            return False
        return (request.user.role == request.user.RoleChoices.VENDOR and 
                request.user.status == request.user.StatusChoices.ACTIVE)
