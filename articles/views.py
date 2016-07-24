from django.shortcuts import redirect, get_object_or_404
from forms import ArticleForm
from models import Article
from django.core.urlresolvers import reverse
from comments.forms import CommentForm
from comments.models import Comment
from tags.models import Tag
from mysite.views import ViewBase

# Create your views here.
class ArticleView(ViewBase):
    def create(self, request):
        if request.method == 'POST':
            article = ArticleForm(request.POST)
            article_instance = article.save(commit=False)
            article_instance.save()
            tags = request.POST.get('tags', None)
            if tags:
                for tag in tags.split():
                    tag_record = Tag.objects.filter(name=tag)
                    if tag_record:
                        tag_record[0].articles.add(article_instance.id)
                    else:
                        tag_record = Tag.objects.create(name=tag)
                        tag_record.articles.add(article_instance.id)
    
            return redirect(reverse(detail, args=[article_instance.id]))
        else:
            form = ArticleForm()
            return self.render(request, 'article_create.html', {'form': form})

    def update(self, request, id):
        article_instance = get_object_or_404(Article, id=id)
        if request.method == 'POST':
            article = ArticleForm(request.POST, instance=article_instance)
            if article.is_valid():
                article.save()

            tags = request.POST.get('tags', None)
            if tags:
                for tag in tags.split():
                    tag_record = Tag.objects.filter(name=tag)
                    if tag_record:
                        tag_record[0].articles.add(article_instance.id)
                    else:
                        tag_record = Tag.objects.create(name=tag)
                        tag_record.articles.add(article_instance.id)

            return redirect(reverse(detail, args=[id]))
        else:

            tags = article_instance.tag_set.all()
            tags = " ".join([tag.name for tag in tags])
            form = ArticleForm(initial={'tags': tags},
                               instance=article_instance)
            return self.render(request, 'article_create.html', {'form': form})

    def detail(self, request, id):
        if request.method == 'POST':
            comment = CommentForm(request.POST)
            commit_instance = comment.save(commit=False)
            commit_instance.article_id = id
            commit_instance.save()
            return redirect(reverse(detail, args=[id]))
    
        article = get_object_or_404(Article, id=id)
        tags = article.tag_set.all()
        comments = Comment.objects.filter(article=article)
        form = CommentForm()
        return self.render(request, 'article_detail.html',
                      {'article': article,
                       'form': form,
                       'comments': comments,
                       'article_tags': tags})

    def list(self, request):
        articles = Article.objects.all()
        return self.render(request, 'article_list.html', {'articles': articles})


av = ArticleView()

def create(request):
    return av.create(request)

def detail(request, id):
    return av.detail(request, id)

def list(request):
    return av.list(request)

def update(request, id):
    return av.update(request, id)

