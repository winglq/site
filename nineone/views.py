from django.shortcuts import render
from nrop19 import nrop19
import uuid
from models import NineoneVideo
from mysite import settings
import os
import logging
from django.views.generic import ListView, DetailView

logger = logging.getLogger(__name__)
# Create your views here.

class NineoneVideoListView(ListView):
    model = NineoneVideo

class NineoneVideoDetailView(DetailView):
    model = NineoneVideo

def test(request):
    return render(request, 'test.html')

def start_download(request):
    n = nrop19()
    infos = n.get_all_video_info_from_url("http://www.91porn.com/v.php?category=tf&viewtype=basic")
    for info in infos:
        if len(NineoneVideo.objects.filter(title=info['title'])):
            logger.info("url %s already exist", info["href"])
            continue
        file_name = "%s.mp4" % uuid.uuid4()
        video_url = n.get_video_url(info['href'])
        n.download_video(video_url, os.path.join(settings.MEDIA_ROOT,
                                                 file_name))
        video = NineoneVideo.objects.create(title=info['title'],
                                            url=video_url,
                                            filename=file_name)
        video.save()

    return render(request, 'test.html')

