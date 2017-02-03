"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, handler404
from django.conf.urls import handler500
from django.contrib import admin
from home.views import index, IndexView
from django.conf.urls.static import static
from django.conf import settings
from favor.views import increase_like_count
from favor.views import increase_dislike_count

handler404 = 'mysite.views.handler404'
handler500 = 'mysite.views.handler500'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^favor/like/(?P<id>[0-9]+)/$', increase_like_count,
        name='like'),
    url(r'^favor/dislike/(?P<id>[0-9]+)/$', increase_dislike_count,
        name='dislike'),
    url(r'^accounts/', include('users.urls')),
    url(r'^register/', include('register.urls')),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^tags/', include('tags.urls')),
    url(r'^articles/', include('articles.urls')),
    url(r'^nineone/', include('nineone.urls')),
    url(r'^ticket/', include('ticket.urls')),
    url(r'^%s/' % settings.XSENDFILE_URL.strip('/'),
        include('xsendfile.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
