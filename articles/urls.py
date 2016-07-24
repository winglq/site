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
from views import create, detail, list, update

urlpatterns = [
    url(r'^create/$', create,
        name='article_create'),
    url(r'^detail/([0-9]{0,10})/$', detail, name='article_detail'),
    url(r'^list/$', list, name='article_list'),
    url(r'^update/([0-9]{0,10})/$', update, name='article_update'),
]
