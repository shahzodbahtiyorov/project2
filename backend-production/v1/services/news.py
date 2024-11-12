#  Unisoft Group Copyright (c) 2024/05/24.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from v1.gateway import metin_gateway
from v1.helper.error_messages import MESSAGE
from v1.models import News, News_Read, SingleNewsModel, AccessToken, Notifications


def get_all(user_id, cms):
    data = {
        "cms": cms
    }
    response = metin_gateway.post(data)
    if response['revokeStatus']:
        return {
            "result": {
                "status": response['status'],
                "message": response['message'],
                "is_revoked": response['revokeStatus'],
            }
        }
    access_token = AccessToken.objects.get(key=user_id)
    user = access_token.user_id
    news = News.objects.all().order_by('-id')
    if not news:
        return {
            "message": MESSAGE['NotData']
        }
    return {
        "result": [new.collection(user) for new in news]
    }


def get_single(user, news_id, cms):
    data = {
        "cms": cms
    }
    response = metin_gateway.post(data)
    if response['revokeStatus']:
        return {
            "result": {
                "status": response['status'],
                "message": response['message'],
                "is_revoked": response['revokeStatus'],
            }
        }
    news = News.objects.filter(id=news_id).first()
    if not news:
        return {
            "message": MESSAGE['NotData']
        }
    return {
        "result": news.collection(user)
    }


def viewed(user, news_id):
    news = News.objects.filter(id=news_id).first()
    if not news:
        return {
            "message": MESSAGE['NotData']
        }
    news.viewed += 1
    news.save()

    news_read = News_Read.objects.filter(news=news_id, user=user).first()
    if not news_read:
        news_read = News_Read()
        news_read.user = user
        news_read.news = news
        news_read.save()
    return {
        "result": news.collection(user)
    }


def likes(user, news_id):
    news = News.objects.filter(id=news_id).first()
    if not news:
        return {
            "message": MESSAGE['NotData']
        }
    news_read = News_Read.objects.filter(news=news_id, user=user).first()
    if news_read:
        if not news_read.liked:
            news.likes += 1
            news.save()
            news_read.liked = True
            news_read.save()
        else:
            news.likes -= 1
            news.save()
            news_read.liked = False
            news_read.save()
    return {
        "result": news.collection(user)
    }


def get_single_news(client, ):
    single_news = SingleNewsModel.objects.filter(client=client)
    return {
        "result": [single_new.collection() for single_new in single_news]
    }


def get_single_news_retrieve(client, single_id):
    single_new_obj = SingleNewsModel.objects.filter(client=client, pk=single_id).first()
    if not single_new_obj:
        return {
            "message": MESSAGE['NotData']
        }
    else:
        single_new_obj.read = 1
        single_new_obj.save()
        return {
            "result": single_new_obj.collection()
        }


def create_single_new(client, text, image=None):
    single_new_obj = SingleNewsModel.objects.create(client=client, question=text, image=image, read=1)
    return {
        "result": single_new_obj.collection()
    }


def get_notification(user_token, cms):
    data = {
        "cms": cms
    }
    response = metin_gateway.post(data)
    if response['revokeStatus']:
        return {
            "result": {
                "status": response['status'],
                "message": response['message'],
                "is_revoked": response['revokeStatus'],
            }
        }
    access_token = AccessToken.objects.select_related('user').get(key=user_token)
    user = access_token.user

    notifications_queryset = Notifications.objects.filter(user=user)
    global_notifications = Notifications.objects.filter(user__isnull=True)

    user_notifications_list = [notification.collection() for notification in notifications_queryset]
    global_notifications_list = [notification.collection() for notification in global_notifications]

    return {
        "result": {
            "user": user_notifications_list,
            "global": global_notifications_list
        }
    }
