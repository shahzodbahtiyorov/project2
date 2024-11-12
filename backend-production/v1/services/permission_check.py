from rest_framework.permissions import BasePermission

from v1.models import RolePermission


class HasChartPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        required_permission = 'chart_permission'

        user_role = request.user.role
        if user_role:
            has_permission = RolePermission.objects.filter(
                role=user_role,
                permission__name=required_permission
            ).exists()

            return has_permission
        return False
