from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_customer:
            return True
        return False


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_employee:
            return True
        return False
