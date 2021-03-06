from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from comments.forms import CommentForm
import uuid
from models import NineoneVideo
from mysite import settings
import os
import logging
from mysite.views import ListView, DetailView, TemplateView
import requests
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from ticket.views import CheckTicketView
from tasks import download_and_save, VideoInfo

logger = logging.getLogger(__name__)
# Create your views here.

def require_ticket(f):
    def inner1(inst, request, *args, **kwargs):
        if not request.user.is_authenticated() and \
                not request.session.get('ticket', None):
            return redirect(reverse('check_ticket',
                                    kwargs={'next': request.path_info}))
        else:
            return f(inst, request, *args, **kwargs)
    return inner1


class NineoneVideoListView(ListView):
    model = NineoneVideo
    paginate_by = 20

    @require_ticket
    def dispatch(self, request, *args, **kwargs):
        return super(NineoneVideoListView, self).dispatch(
            request, *args, **kwargs)
    def get_queryset(self):
        order = self.request.GET.get('orderby')
        videoes = NineoneVideo.objects.all()
        if order:
            videoes = videoes.order_by("-"+order)
        return videoes

class NineoneVideoDetailView(DetailView):
    model = NineoneVideo

    @require_ticket
    def dispatch(self, request, *args, **kwargs):
        return super(NineoneVideoDetailView, self).dispatch(
            request, *args, **kwargs)

    @require_ticket
    def post(self, request, pk):
        self.object = get_object_or_404(NineoneVideo, id=pk)
        comment = CommentForm(request.POST)
        commit_instance = comment.save()
        self.object.comments.add(commit_instance)
        self.object.save()
        return redirect(reverse('nineone_detail', args=[pk]))


class VideoDownloadView(TemplateView):
    template_name = 'nineone/nineone_download_info.html'

    def get(self, request, *args, **kwargs):
        logging.debug("enter: VideoDownloadView.get")
        download_and_save()
        context = super(VideoDownloadView, self). \
            get_context_data(**kwargs)
        vinfo = VideoInfo()
        context['object_list'] = vinfo.get_obj_list()
        return self.render_to_response(context)

def get_all_unused_files():
    all_video = [ x.filename for x in NineoneVideo.objects.all() ]
    print "all video: %s" % len(all_video)
    print "all files: %s" % len(os.listdir(settings.XSENDFILE_ROOT))
    unused_files = [ x for x in os.listdir(settings.XSENDFILE_ROOT) if x not in all_video]
    print "all unused_files: %s" % len(unused_files)
    return unused_files

def clean(request):
    unused_files = get_all_unused_files()
    print unused_files
    for f in unused_files:
        os.remove(os.path.join(settings.XSENDFILE_ROOT, f))
        print "removed file: %s" % os.path.join(settings.XSENDFILE_ROOT, f)


