from rest_framework import permissions


class CustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.data.get("is_customer"):
            return False
        return True


class EmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.data.get("is_employee"):
            return False
        return True
