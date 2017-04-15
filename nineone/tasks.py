from __future__ import absolute_import

from celery import shared_task
from .models import NineoneVideo
from django.conf import settings
from .nrop19 import nrop19
import logging
logger = logging.getLogger(__name__)
import uuid
import os
from django.http import Http404


def singleton_instance(cls):
    instances = {}
    def inner(*args, **kwargs):
        if not instances.get(cls, None):
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return inner

class A(object):
    pass

@singleton_instance
class VideoInfo(object):
    def __init__(self):
        self.videos = {}

    def update(self, video, status):
        if status == 'completed':
            del self.videos[video]
        else:
            self.videos[video] = status

    def clear(self):
        self.videos = {}

    def get(self, video):
        return self.videos.get(video, None)

    def get_obj_list(self):
        l = []
        for k, v in self.videos.iteritems():
            o = A()
            o.name = k
            o.status = v
            l.append(o)
        return l


n = nrop19()
@shared_task
def download_single(title, video_url, filename):
    vinfo = VideoInfo()
    vinfo.update(title, 'downloading')
    n.download_video2(video_url, os.path.join(settings.XSENDFILE_ROOT,
                                              filename))
    video = NineoneVideo.objects.create(title=title,
                                        url=video_url,
                                        filename=filename)
    video.save()


def download_and_save():
    logging.debug("enter download_and_save")
    vinfo = VideoInfo()
    #infos = n.get_all_video_info_from_url("http://68.235.35.99/v.php?category=mf&viewtype=basic&page=8")
    infos = n.get_all_video_info_from_url("http://68.235.35.99/v.php?category=tf&viewtype=basic")
    #infos = n.get_all_video_info_from_url("http://68.235.35.99/v.php?category=top&m=-2&viewtype=basic")
    #infos = n.get_all_video_info_from_url("http://email.91dizhi.at.gmail.com.7h4.space/v.php?category=tf&viewtype=basic")
    #infos = n.get_all_video_info_from_url("http://sh.k7p.work/v.php?category=tf&viewtype=basic")
    #infos = n.get_all_video_info_from_url("http://sh.k7p.work/v.php?category=top&m=-1&viewtype=basic")
    #infos = n.get_all_video_info_from_url("http://sh.k7p.work/v.php?category=mf&viewtype=basic&page=2")
    for info in infos:
        if info['title'] not in vinfo.videos:
            vinfo.update(info['title'], 'waiting')

    for info in infos:
        if len(NineoneVideo.objects.filter(title=info['title'])):
            logger.info("url %s already exist", info["href"])
            vinfo.update(info['title'], 'completed')
            continue
        if vinfo.get(info['title']) == 'downloading':
            logger.info("url %s is already in downloading", info["href"])
            continue
        file_name = "%s.mp4" % uuid.uuid4()
        try:
            video_url = n.get_video_url(info['href'])
        except Exception as e:
            logger.info("Download %s failed. Due to %s", info['href'], str(e))
            break
        logger.info('begin to delay download title %s', info['title'])
        download_single.delay(info['title'], video_url, file_name)
