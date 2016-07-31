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
from views import create, new, list_registerred, list
urlpatterns = [
    url(r'^create/$', create,
        name='register_create'),
    url(r'^new/([0-9a-f]{32})/$', new, name='register_new'),
    url(r'^list/([0-9a-f]{32})/$', list_registerred, name='register_list'),
    url(r'^list/$', list, name='register_list_meta'),
]
