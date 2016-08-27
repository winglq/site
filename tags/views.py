from django.shortcuts import render
from models import Tag
from articles.views import ArticleListView
from mysite.views import ViewBase

# Create your views here.

class TagView(ViewBase):
    def show(self, request, id):
        return ArticleListView.as_view(tag_id=id)(request)

def show(request, id):
    return TagView().show(request, id)

