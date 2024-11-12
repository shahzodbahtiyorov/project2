import random
import uuid

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from v1.models import Users, RolePermission, MFO, PurposeCode, Document_type, Role, News, Permission, \
    ClientInfo, ClientIABSAccount, DocHistories


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name']


class RolePermissionSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    permission = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all())

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission']


class MFOSerializer(serializers.ModelSerializer):
    class Meta:
        model = MFO
        fields = ['id', 'code', 'name']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name']


class AccoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientIABSAccount
        fields = ['client', 'name', 'number', 'is_primary', 'is_report', 'is_document', 'balance', 'mfo']


class CompanySerializer(serializers.ModelSerializer):
    mfo = MFOSerializer(read_only=True)
    director = DirectorSerializer(read_only=True)
    account = AccoutsSerializer(many=True, read_only=True)

    class Meta:
        model = ClientInfo
        fields = ['id', 'client_name', 'mfo', 'director', 'accountant', 'account']


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientInfo
        fields = ['id', 'client_name']


class UserSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False)
    role_name = serializers.SerializerMethodField()
    workspace = WorkspaceSerializer(read_only=True)
    login = serializers.SerializerMethodField()
    agreement = serializers.SerializerMethodField()
    client_code = serializers.SerializerMethodField()
    key = serializers.SerializerMethodField()
    oko = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'username', 'phone_number', 'first_name', 'last_name', 'email', 'avatar',
                  'is_test', 'is_staff', 'is_superuser', 'is_active', 'identity', 'permissions', 'created_at',
                  'updated_at', 'birth_date', 'salary', 'login', 'agreement', 'client_code',
                  'workspace', 'role', 'role_name', 'password', 'key', 'oko']

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role_data = validated_data.pop('role', None)
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = make_password(password)
        user = Users.objects.create(**validated_data)

        if role_data:
            user.role = Role.objects.get(id=role_data)
            user.save()

        return user

    def update(self, instance, validated_data):
        role_data = validated_data.pop('role', None)
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.password = make_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if role_data:
            instance.role = Role.objects.get(id=role_data.id)

        instance.save()
        return instance

    def get_role_name(self, obj):
        if obj.role is None:
            return None
        return obj.role.name

    def get_login(self, obj):
        return f"{uuid.uuid4().hex[:12]}"

    def get_agreement(self, obj):
        return f"U{random.randint(100, 999)}"

    def get_client_code(self, obj):
        return f"{random.randint(10000000, 99999999)}"

    def get_key(self, obj):
        return f"MLS{random.randint(1000, 9999)}"

    def get_oko(self, obj):
        return 'Нет'


class PasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords must match.")
        return data


class PurposeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeCode
        fields = ['id', 'code', 'name']


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_type
        fields = ['id', 'name']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title_uz', 'title_ru', 'title_en', 'desc_uz', 'desc_en', 'desc_ru',
                  'body_uz', 'body_en', 'body_ru', 'link', 'viewed', 'likes',
                  'status', 'created_at', 'updated_at']


class ChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocHistories
        fields = ['credit_amount', 'debit_amount', 'transaction_date', 'receiver_mfo']


class UserRoleSerializer(serializers.ModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = Users
        fields = ['id', 'role']


class CompanyUserSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['id', 'username', 'role_name', 'phone_number', 'email', 'first_name', 'last_name']

    def get_role_name(self, obj):
        if obj.role is None:
            return None
        return obj.role.name


class ClientSerializer(serializers.ModelSerializer):
    user = CompanyUserSerializer()
    key = serializers.SerializerMethodField()
    oko = serializers.SerializerMethodField()

    class Meta:
        model = ClientInfo
        fields = ['id',
                  'branch_code',
                  'branch_name',
                  'devision_code',
                  'devision_name',
                  'client_code',
                  'client_name',
                  'direction_code',
                  'direction_name',
                  'user',
                  'contract_date',
                  'contract_number',
                  'director',
                  'accountant',
                  'is_active',
                  'key',
                  'oko',
                  'updated_at']

    def get_key(self, obj):
        return f"MLS{random.randint(1000, 9999)}"

    def get_oko(self, obj):
        return "Нет"

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_instance = instance.user
            user_serializer = CompanyUserSerializer(user_instance, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()

        return super().update(instance, validated_data)


class ClientAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientIABSAccount
        fields = ['id', 'number', 'name', 'is_active', 'is_document', 'is_report']


class AdminPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("New passwords must match.")
        return data


class AllAccoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientIABSAccount
        fields = ['id', 'number', 'name', 'is_active', 'inn', 'mfo', 'iabs_id', 'is_report', 'is_document']


class DashboardStaff(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'phone_number', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        representation.pop('is_staff', None)
        return representation
