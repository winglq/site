from django.shortcuts import render
from django.http import HttpResponse
from models import HomeArticle
# Create your views here.
def index(request):
    article = list(HomeArticle.objects.all())[-1].article
    return render(request, "index.html", {'article': article})
