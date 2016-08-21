from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from mysite import settings
from django.http import Http404

# Create your views here.
def require_ticket(f):
    def inner1(request, *args, **kwargs):
        if not request.user.is_authenticated() and \
                not request.session.get('ticket', None):
            raise Http404()
        else:
            return f(request, *args, **kwargs)
    return inner1

@require_ticket
def xsendfile(request, filename):
    response = HttpResponse()
    response['X-Accel-Redirect'] = ('/%s/%s' % (settings.XSENDFILE_NGINX_URL.strip('/'),
                                                filename)).encode('utf-8')
    return response
