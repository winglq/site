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
from django.conf.urls import url, include
from views import VideoDownloadView
from views import NineoneVideoListView, NineoneVideoDetailView
from views import clean
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^sdownload/$',
        login_required(VideoDownloadView.as_view()),
        name="sdownload"),
    url(r'^list/$', NineoneVideoListView.as_view(),
        name='nineone_list'),
    url(r'^detail/(?P<pk>[0-9]+)$', NineoneVideoDetailView.as_view(),
        name="nineone_detail"),
    url(r'^clean/$',
        login_required(clean),
        name='clean_nineone'),
]
