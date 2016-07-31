from django.shortcuts import render
from models import Tag
from mysite.views import ViewBase

# Create your views here.

class TagView(ViewBase):
    def show(self, request, id):
        tag = Tag.objects.filter(id=id)[0]
        return self.render(request, "article_list.html", {'articles': tag.articles.all()})

def show(request, id):
    return TagView().show(request, id)

