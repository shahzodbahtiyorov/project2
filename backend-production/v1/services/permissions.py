from sqlite3 import IntegrityError

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response

from v1.models.users import Permission, RolePermission, Users, Role
from v1.serializers import PermissionSerializer, RoleSerializer, RolePermissionSerializer, UserRoleSerializer


class CreatePermission(GenericAPIView):
    serializer_class = PermissionSerializer

    @swagger_auto_schema(
        operation_description="Get all Permission",
        responses={
            200: openapi.Response('Permission', openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response('Permission not found')
        }
    )
    def get(self, request, pk=None):
        if pk:
            permission = Permission.objects.get(pk=pk)
            serializer = self.serializer_class(permission)
            return Response({'success': serializer.data})

        permissions = Permission.objects.all()
        serializer = self.serializer_class(permissions, many=True)
        return Response({"success": serializer.data})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        permission = Permission.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data, partial=True, instance=permission)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": serializer.data})

    def delete(self, request, pk=None):
        permission = Permission.objects.get(pk=pk)
        if permission:
            permission.delete()
            return Response({'success': True})
        return Response({'success': False})


class CreateRoleView(GenericAPIView):
    serializer_class = RoleSerializer

    @swagger_auto_schema(
        operation_description="Get all Roles",
        responses={
            200: openapi.Response('Roles', openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response('Role not found')
        }
    )
    def get(self, request, pk=None):
        if pk:
            role = Role.objects.get(pk=pk)
            serializer = self.serializer_class(role)
            return Response({'success': serializer.data})

        roles = Role.objects.all()
        serializer = self.serializer_class(roles, many=True)
        return Response({"success": serializer.data})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": serializer.data})

    def put(self, request, pk=None):
        role = Role.objects.get(pk=pk)
        serializer = self.serializer_class(role, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": serializer.data})

    def delete(self, request, pk=None):
        role = Role.objects.get(pk=pk)
        if role:
            role.delete()
            return Response({"success": True})
        return Response({"success": False})


class PermissionToRoleView(GenericAPIView):
    serializer_class = RolePermissionSerializer

    @swagger_auto_schema(
        operation_description="Get all permissions for a specific role or all role-permission mappings",
        responses={
            200: openapi.Response('Permissions to Role', openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response('Not found')
        }
    )
    def get(self, request, pk=None):
        if pk:
            role = get_object_or_404(Role, pk=pk)
            role_permissions = RolePermission.objects.filter(role=role).select_related('permission')
            role_permissions_data = {
                'role': role.pk,
                'permissions': [per.permission.name for per in role_permissions]
            }
            return Response({"success": role_permissions_data}, status=status.HTTP_200_OK)

        role_permissions = RolePermission.objects.select_related('role', 'permission')
        serializer = self.get_serializer(role_permissions, many=True)
        return Response({"success": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        role_id = request.data.get('role')
        permission_ids = request.data.get('permissions', [])

        role, created = Role.objects.get_or_create(name=role_id)

        created_permissions = []
        errors = []

        for perm_id in permission_ids:
            permission = get_object_or_404(Permission, pk=perm_id)
            if RolePermission.objects.filter(role=role, permission=permission).exists():
                errors.append(f"Mapping for role {role_id} and permission {perm_id} already exists.")
                continue

            role_permission = RolePermission.objects.create(role=role, permission=permission)
            created_permissions.append(role_permission)

        if created_permissions:
            response_serializer = RolePermissionSerializer(created_permissions, many=True)
            return Response({"success": response_serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"error": errors or "No permissions were created."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk is None:
            return Response({"error": "Role ID must be provided"}, status=status.HTTP_400_BAD_REQUEST)

        role = get_object_or_404(Role, pk=pk)
        permission_ids = request.data.get('permissions', [])

        permissions = []
        for perm_id in permission_ids:
            permission = get_object_or_404(Permission, pk=perm_id)
            permissions.append(permission)

        try:
            RolePermission.objects.filter(role=role).delete()

            created_permissions = []
            for permission in permissions:
                role_permission = RolePermission.objects.create(role=role, permission=permission)
                created_permissions.append(role_permission)

            response_serializer = RolePermissionSerializer(created_permissions, many=True)
            return Response({"success": response_serializer.data}, status=status.HTTP_200_OK)

        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        role_permission = get_object_or_404(RolePermission, pk=pk)
        role_permission.delete()
        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)


class UserRoleView(GenericAPIView):
    serializer_class = UserRoleSerializer

    def post(self, request):
        user = Users.objects.filter(id=request.data['user_id']).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        role = Role.objects.filter(id=request.data['role']).first()
        if not role:
            return Response({"error": "Role not found"}, status=status.HTTP_400_BAD_REQUEST)

        user.role = role
        user.save()

        return Response({
            "success": True,
            "user": user.username,
            "role": role.name
        })

