from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    bookmark_videos = models.ManyToManyField(
        'video.Video',
        blank=True,
        through='BookmarkVideo',
        # 기본 값 : myuser_set
        related_name='bookmark_user_set'
    )


class BookmarkVideo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    video = models.ForeignKey('video.Video')
    create_date = models.DateTimeField(auto_now_add=True)

    # migration 에러를 해결하기 위해 db_table 이름을 설정한 후
    # --fake 옵션을 주어 migration
    # $./manage.py migrate member --fake
    # db_table은 만들어져 있는 db_table 이름 필드이름과 동일하게 한다.
    # class Meta:
    #     db_table = 'member_myuser_bookmark_videos'
