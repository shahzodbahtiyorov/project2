import json

from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.firebase import db, send_notification
from v1.models import Device, News, Notifications
from v1.serializers import NewsSerializer


def save_token(request):
    data = json.loads(request.body)
    token = data.get('token')
    user_id = data.get('user_id')

    db.collection('device_tokens').document(user_id).set({
        'token': token,
        'timestamp': datetime.utcnow()
    })


class SendToDeviceView(GenericAPIView):
    @swagger_auto_schema(
        operation_description="Sends notification to device from firebase",
        responses={
            200: openapi.Response('Notification', openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response('token not found')
        }
    )
    def post(self, request, *args, **kwargs):
        user = request.data['user_id']
        firebase_token = Device.objects.filter(user_id=user).first()
        title = request.data['title']
        body = request.data['body']
        if not firebase_token:
            return Response({"Error": "Firebase token not found"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            "message": {
                "token": firebase_token.firebase_reg_id,
                "notification": {
                    "title": title,
                    "body": body,
                }
            }
        }

        response = send_notification(payload)
        if 'name' in response:
            Notifications.objects.create(
                user_id=user,
                title=title,
                body=body,
            )

        return Response({"result": f'Success {response}'}, status=status.HTTP_200_OK)


class SendTopicView(GenericAPIView):

    @swagger_auto_schema(
        operation_description="Send notification to Topic from firebase",
        responses={
            200: openapi.Response('Topic', openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response('Topic not found')
        }
    )
    def post(self, request, *args, **kwargs):
        topic = request.data['topic']
        title = request.data['title']
        body = request.data['body']
        story_id = request.data['story_id']
        payload = {
            "message": {
                "topic": topic,
                "notification": {
                    "title": title,
                    "body": body,
                },
                "data": {
                    "story_id": story_id,
                }
            }
        }
        response = send_notification(payload)
        if 'name' in response:
            Notifications.objects.create(device=topic, title=title, body=body, story_id=story_id)

        return Response({"result": f'Success {response}'}, status=status.HTTP_200_OK)


class NewsView(GenericAPIView):
    serializer_class = NewsSerializer

    @swagger_auto_schema(
        operation_description="Get all news",
        responses={
            200: openapi.Response('News', openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response('News not found')
        }
    )
    def get(self, request, *args, **kwargs):
        news = News.objects.all().select_related('user_id')

        serializer = self.serializer_class(news, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create new news",
        responses={
            200: openapi.Response('News', openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response('fields required to fill')
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update existing news",
        responses={
            200: openapi.Response('News', openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response('news not found')
        }
    )
    def put(self, request, pk=None):
        news = News.objects.get(pk=pk)
        serializer = self.serializer_class(data=request.data, partial=True, instance=news)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        news = News.objects.get(pk=pk)
        if not news:
            return Response({"Error": "News not found"}, status=status.HTTP_400_BAD_REQUEST)

        news.delete()
        return Response({"result": "Success"}, status=status.HTTP_200_OK)
