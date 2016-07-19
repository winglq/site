from django.shortcuts import render, redirect
from forms import ArticleForm
from models import Article
from django.core.urlresolvers import reverse

# Create your views here.
def create(request):
    if request.method == 'POST':
        article = ArticleForm(request.POST)
        article_instance = article.save(commit=False)
        article_instance.save()
        return redirect(reverse(detail, args=[article_instance.id]))
    else:
         form = ArticleForm()
         return render(request, 'article_create.html', {'form': form})

def detail(request, id):
    article = Article.objects.filter(id=id)[0]
    return render(request, 'article_detail.html', {'article': article})

def list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

