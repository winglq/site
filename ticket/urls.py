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
from views import generate, TicketListView, check
from views import  TicketListAvailableView, check
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^gen/$', generate,
        name='generate_ticket'),
    url(r'^list/$', TicketListAvailableView.as_view(),
        name="list_ticket"),
    url(r'^check/([0-9\-a-f]{36})$', check,
        name='check_ticket'),
    url(r'^check/(?P<next>/.*)$', check,
        name='check_ticket'),
    url(r'^check/$', check,
        name='check_ticket'),
    url(r'^list_all/$', login_required(TicketListView.as_view()),
        name='list_all_ticket')
]
