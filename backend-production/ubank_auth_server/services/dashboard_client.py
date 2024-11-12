from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response

from api.firebase import send_notification
from v1.models import Device, DocumentRegistration, Notifications, ClientInfo

from ubank_auth_server.serilizers import UserDeviceSerializer, DocumentViewSerializer, SpecificCompanySerializer, \
    AllCompanySerializer


class UserSession(GenericAPIView):
    company_serializer_class = AllCompanySerializer
    specific_company_serializer_class = SpecificCompanySerializer

    def get(self, request, pk=None):
        if pk:
            company = ClientInfo.objects.select_related('user').prefetch_related('user__device').filter(
                pk=pk).first()
            company_serializer = self.specific_company_serializer_class(company)

            return Response({"success": {"company": company_serializer.data}}, status=status.HTTP_200_OK)

        companies = ClientInfo.objects.select_related('user').all()
        company_serializer = self.company_serializer_class(companies, many=True)

        return Response({"success": {"companies": company_serializer.data}}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        device = Device.objects.select_related('user').filter(pk=pk).first()
        if device is None:
            return Response({"success": False, "message": "Device not found"}, status=404)

        if 'is_blocked' in request.data and request.data['is_blocked'] is False:
            device.tries = 0

        serializer = UserDeviceSerializer(device, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            update_device = serializer.save()

        user = update_device.user
        verified = update_device.verified
        if not verified:
            return Response({"success": True, "data": serializer.data})

        title = "Статус устройства обновлен"
        body = "Вы прошли верификацию"
        firebase_token = update_device.firebase_reg_id

        payload = {
            "message": {
                "token": firebase_token,
                "notification": {
                    "title": title,
                    "body": body,
                }
            }
        }

        response = send_notification(payload)
        if 'name' in response:
            Notifications.objects.create(
                user_id=user.id,
                title=title,
                body=body,
            )

        return Response({"success": True, "data": serializer.data})


def delete(self, request, pk):
    device = Device.objects.select_related('user').filter(pk=pk).first()
    if device is None:
        return Response({"success": False, "message": "Device not found"}, status=404)
    device.delete()
    return Response({"success": True, "data": "deleted successfully"})


class DocumentView(GenericAPIView):
    serializer_class = DocumentViewSerializer

    def get(self, request, pk=None):
        if pk:
            try:
                client = ClientInfo.objects.select_related('user').filter(id=pk).first()
                if client is None:
                    return Response({"success": False, "message": "Client not found"}, status=404)
                print(client.user.phone_number)
                document = DocumentRegistration.objects.get(phone_number=client.user.phone_number)
                serializer = self.serializer_class(document)
                return Response({"success": True, "data": serializer.data})
            except DocumentRegistration.DoesNotExist:
                return Response({"success": False, "message": "Document not found"}, status=404)

        documents = DocumentRegistration.objects.all()
        serializer = self.serializer_class(documents, many=True)
        return Response({"success": True, "data": serializer.data})
