import ipaddress

import pycountry
import requests
from rest_framework import serializers
from ip2geotools.databases.noncommercial import DbIpCity
from v1.models import Device, Users, DocumentRegistration, ClientInfo
from django.core.cache import cache


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientInfo
        fields = ['client_name', 'certificate']


class UserDeviceSerializer(serializers.ModelSerializer):
    client = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = Device
        fields = ['id', 'client', 'location', 'uuid', 'name', 'core_id', 'firebase_reg_id', 'version', 'verified', 'is_blocked']

    def get_client(self, obj):
        user = obj.user
        if hasattr(user, 'client'):
            return ClientSerializer(user.client).data
        return None

    def is_private_ip(self, ip):
        return ipaddress.ip_address(ip).is_private

    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org?format=json')
            return response.json().get('ip')
        except requests.RequestException:
            return None

    def get_location(self, obj):
        ip_address = obj.ip

        if self.is_private_ip(ip_address):
            ip_address = self.get_public_ip()

        cache_key = f'location_{ip_address}'
        location = cache.get(cache_key)

        if location is None:
            try:
                response = DbIpCity.get(ip_address, api_key='free')
                country_code = response.country
                city = response.city
                region = response.region

                country = pycountry.countries.get(alpha_2=country_code)
                country_name = country.name if country else "Unknown"

                location = {
                    "country": country_name,
                    "city": city,
                    "region": region
                }

                cache.set(cache_key, location, timeout=3600)

            except Exception:
                location = {
                    "country": "Unknown",
                    "city": "Unknown",
                    "region": "Unknown"
                }
                cache.set(cache_key, location, timeout=3600)

        return location


class UserSessionSerializer(serializers.ModelSerializer):
    devices = UserDeviceSerializer(many=True, read_only=True, source='device')

    class Meta:
        model = Users
        fields = ['id', 'username', 'devices']


class SpecificCompanySerializer(serializers.ModelSerializer):
    user = UserSessionSerializer(read_only=True)

    class Meta:
        model = ClientInfo
        fields = ['id', 'client_name', 'user']


class DirectorNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name']


class AllCompanySerializer(serializers.ModelSerializer):
    user = DirectorNameSerializer(read_only=True)

    class Meta:
        model = ClientInfo
        fields = ['id', 'client_name', 'user']


class DocumentViewSerializer(serializers.ModelSerializer):
    entity_name = serializers.SerializerMethodField()

    class Meta:
        model = DocumentRegistration
        fields = ['id', 'phone_number', 'user_type', 'entity_name', 'pinfil', 'tin', 'passport_front', 'passport_back',
                  'licence_certificate', 'order_proxy', 'status', 'created_at']

    def get_entity_name(self, obj):
        return DocumentRegistration.UserType(obj.user_type).label
