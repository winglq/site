from __future__ import unicode_literals
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.db import models
from mysite import settings

import os
import logging

logger = logging.getLogger(__name__)

# Create your models here.
class NineoneVideo(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=512)
    url = models.URLField()
    ctime = models.DateTimeField('create time', auto_now_add=True, blank=True)
    filename = models.CharField(max_length=512)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-ctime']

@receiver(post_delete, sender=NineoneVideo)
def delete_video_file(sender, instance, **kwargs):
    f = os.path.join(settings.XSENDFILE_ROOT, instance.filename)
    os.remove(f)
    logger.info("%s deleted", f)


