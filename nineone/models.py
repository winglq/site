from __future__ import unicode_literals

from django.db import models

# Create your models here.
class NineoneVideo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=512)
    url = models.URLField()
    ctime = models.DateTimeField('create time', auto_now_add=True, blank=True)
    filename = models.CharField(max_length=512)
