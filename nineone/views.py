from django.shortcuts import render, redirect
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
from tasks import download_and_save

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

class VideoDownloadView(TemplateView):
    def get(self, request, *args, **kwargs):
        download_and_save.delay()
        return redirect('/nineone/list')
