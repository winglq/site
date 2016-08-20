from django.shortcuts import render, redirect
from nrop19 import nrop19
import uuid
from models import NineoneVideo
from mysite import settings
import os
import logging
from mysite.views import ListView, DetailView
import requests
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from ticket.views import check

logger = logging.getLogger(__name__)
# Create your views here.

def require_ticket(f):
    def inner1(inst, request, *args, **kwargs):
        if not request.user.is_authenticated() and \
                not request.session.get('ticket', None):
            return redirect(reverse(check,
                                kwargs={'next': request.path_info}))
        else:
            return f(inst, request, *args, **kwargs)
    return inner1


class NineoneVideoListView(ListView):
    model = NineoneVideo

    @require_ticket
    def dispatch(self, request, *args, **kwargs):
        return super(NineoneVideoListView, self).dispatch(
            request, *args, **kwargs)

class NineoneVideoDetailView(DetailView):
    model = NineoneVideo

    @require_ticket
    def dispatch(self, request, *args, **kwargs):
        return super(NineoneVideoDetailView, self).dispatch(
            request, *args, **kwargs)

def test(request):
    return render(request, 'test.html')

def start_download(request):
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
                n.download_video2(video_url, os.path.join(settings.MEDIA_ROOT,
                                                         file_name))
                break
            except requests.exceptions.ChunkedEncodingError as e:
                logger.error("download video fail. reason: %s left retries: %s",
                             str(e), retries)
                --retries
        video = NineoneVideo.objects.create(title=info['title'],
                                            url=video_url,
                                            filename=file_name)
        video.save()

    return render(request, 'test.html')

