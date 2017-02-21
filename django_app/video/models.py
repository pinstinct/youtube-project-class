from django.db import models


class VideoInfo(models.Model):
    video_id = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    published_date = models.DateTimeField(null=True, blank=True)
