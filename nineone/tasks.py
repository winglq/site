from __future__ import absolute_import

from celery import shared_task
from .models import NineoneVideo
from django.conf import settings
from .nrop19 import nrop19
import logging
logger = logging.getLogger(__name__)
import uuid
import os

@shared_task
def download_and_save():
    n = nrop19()
    infos = n.get_all_video_info_from_url("http://sh.k7p.work/v.php?category=tf&viewtype=basic")
    for info in infos:
        if len(NineoneVideo.objects.filter(title=info['title'])):
            logger.info("url %s already exist", info["href"])
            continue
        file_name = "%s.mp4" % uuid.uuid4()
        video_url = n.get_video_url(info['href'])
        retries = 5
        while retries > 0:
            try:
                n.download_video2(video_url, os.path.join(settings.XSENDFILE_ROOT,
                                                         file_name))
                break
            except Exception as e:
                logger.error("download video fail. reason: %s left retries: %s",
                             str(e), retries)
                retries -= 1
        video = NineoneVideo.objects.create(title=info['title'],
                                            url=video_url,
                                            filename=file_name)
        video.save()
