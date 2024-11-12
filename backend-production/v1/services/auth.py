#  Unisoft Group Copyright (c) 2024/05/24.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from v1.helper.helper import is_valid_password
from v1.models import Users, AccessToken
from v1.serializers import UserSerializer, PasswordChangeSerializer, AdminPasswordChangeSerializer, DashboardStaff


class CreateStaff(GenericAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Create a new staff member",
        request_body=UserSerializer,
        responses={201: UserSerializer}
    )
    def post(self, request):
        user_requirements = ['username', 'phone_number', 'password', 'first_name', 'last_name', 'email', 'avatar',
                             'is_test', 'is_staff', 'is_active']
        for field in user_requirements:
            if field not in request.data:
                return Response({'required': field}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Success": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"Error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Retrieve a staff member or list of staff members",
        responses={
            200: UserSerializer(many=True),
            404: openapi.Response('User not found')
        }
    )
    def get(self, request, pk=None):
        if pk:
            try:
                user = Users.objects.get(pk=pk)
            except Users.DoesNotExist:
                return Response({"Error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(user)
            return Response({"Success": serializer.data}, status=status.HTTP_200_OK)

        users = Users.objects.filter(is_superuser=False).all()
        serializer = self.get_serializer(users, many=True)
        return Response({"Success": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update a staff member",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            404: openapi.Response('User not found')
        }
    )
    def put(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)

        except Users.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data, partial=True, instance=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response({
            "Success": serializer.data
        })

    @swagger_auto_schema(
        operation_description="Delete a staff member",
        responses={
            204: openapi.Response('User deleted'),
            404: openapi.Response('User not found')
        }
    )
    def delete(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
            print(user)
            user.delete()
        except Users.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "Success": True
        }, status=status.HTTP_200_OK)


class UserLogin(GenericAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Login User",
        responses={
            200: openapi.Response('User logged in successfully'),
            401: openapi.Response('Incorrect username or password'),
            404: openapi.Response('User not found'),
        }
    )
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = Users.objects.filter(username=username, is_staff=True).first()

        if not user:
            return Response({'error': 'Incorrect username or password'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'error': 'Incorrect username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        access_token, created = AccessToken.objects.get_or_create(user=user)

        return Response({
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "access_token": access_token.key if user.is_staff else None,
            "fullname": f'{user.first_name} {user.last_name}',
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role.name,
        })


class PasswordChangeView(GenericAPIView):
    serializer_class = PasswordChangeSerializer

    @swagger_auto_schema(
        operation_description="Change User Password",
        request_body=PasswordChangeSerializer,
        responses={
            200: openapi.Response('Password changed successfully'),
            400: openapi.Response('Invalid input'),
            401: openapi.Response('Incorrect password'),
        }
    )
    def post(self, request):
        user = Users.objects.filter(username=request.data['username']).first()
        if not user:
            return Response({'error': 'incorrect username'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']

        user.password = make_password(new_password)
        user.save()

        return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)


class AdminPasswordChangeView(GenericAPIView):
    serializer_class = AdminPasswordChangeSerializer

    @swagger_auto_schema(
        operation_description="Change User Password",
        request_body=PasswordChangeSerializer,
        responses={
            200: openapi.Response('Password changed successfully'),
            400: openapi.Response('Invalid input'),
            401: openapi.Response('Incorrect old password'),
        }
    )
    def post(self, request):
        user_token = request.headers.get('Authorization').split(' ')[1]

        if not user_token:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        user = AccessToken.objects.select_related('user').get(key=user_token).user

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not check_password(old_password, user.password):
            return Response({'error': 'Incorrect old password'}, status=status.HTTP_401_UNAUTHORIZED)

        user.password = make_password(new_password)
        user.save()

        return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)


class CreateDashboardStaff(GenericAPIView):
    serializer_class = DashboardStaff

    def get(self, request):
        staff = Users.objects.filter(is_staff=True).all()
        serializer = self.serializer_class(staff, many=True)
        return Response({'staff': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        user = Users.objects.filter(username=request.data['username']).first()
        if user:
            return Response({'error': 'user with this username already exists'}, status=status.HTTP_404_NOT_FOUND)

        if not is_valid_password(request.data['password']):
            return Response({
                "error": "Password is invalid. It must be at least 8 characters long and contain letters, numbers, and symbols."},
                status=status.HTTP_400_BAD_REQUEST)
        user_data = request.data.copy()
        user_data['is_staff'] = True
        user_data['is_active'] = True
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': 'Created'}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        staff = Users.objects.filter(id=pk).first()
        if not staff:
            return Response({'error': 'user with this id does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(staff, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': 'Updated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
