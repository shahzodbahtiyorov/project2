#  Unisoft Group Copyright (c) 2023/1/26.
#
#  Created by Mahmudov Abdulloh
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from uuid import uuid4
from django.db import models
from v1.models import Users


def upload_location(instance, filename):
    ext = filename.split('.')[-1]
    if ext.lower() in ['doc', 'png', 'pdf', 'xml', 'jpeg', 'mp4', 'jpg', 'mov', 'm4v']:
        file_path = 'news/{title}'.format(title='{}.{}'.format(uuid4().hex, ext))
        return file_path
    else:
        raise Exception


class News(models.Model):
    title_uz = models.CharField(max_length=255)
    title_ru = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    desc_uz = models.TextField()
    desc_en = models.TextField()
    desc_ru = models.TextField()
    body_uz = models.TextField()
    body_en = models.TextField()
    body_ru = models.TextField()
    link = models.CharField(max_length=255, null=True)  # ?
    viewed = models.IntegerField(default=0)  # ?
    likes = models.IntegerField(default=0)  # ?
    status = models.IntegerField(default=0)  # ?
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "News"

    def collection(self, user=None):
        news = News_Read.objects.filter(user=user, news_id=self.id).first()
        if news:
            read = True
            liked = news.liked
        else:
            read = False
            liked = False
        return {
            'id': self.id,
            'title_uz': self.title_uz,
            'title_ru': self.title_ru,
            'title_en': self.title_en,
            'desc_uz': self.desc_uz,
            'desc_en': self.desc_en,
            'desc_ru': self.desc_ru,
            'body_uz': self.body_uz,
            'body_en': self.body_en,
            'body_ru': self.body_ru,
            'link': self.link,
            'is_read': read,
            'is_like': liked,
            'viewed': self.viewed,
            'likes': self.likes,
            'created_at': self.created_at.strftime("%d %b, %Y"),
            'updated_at': self.updated_at.strftime("%d %b, %Y"),
        }


class News_Read(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="news_read")
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news")
    liked = models.BooleanField(default=False)  # ?


class Notifications(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="notifications", null=True)
    device = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255, null=True)
    story_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def collection(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'story_id': self.story_id,
            'created_at': self.created_at.strftime('%d.%m.%Y'),
        }
