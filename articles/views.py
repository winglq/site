from django.shortcuts import redirect, get_object_or_404
from forms import ArticleForm
from models import Article
from django.core.urlresolvers import reverse
from comments.forms import CommentForm
from comments.models import Comment
from tags.models import Tag
from mysite.views import DetailView, ListView
from mysite.views import CreateView, UpdateView


class ArticleUpdateView(UpdateView):
    model = Article
    template_name_suffix = '_create'
    fields = []

    def get_form(self):
        tags = self.object.tags.all()
        tags = " ".join([tag.name for tag in tags])
        form = ArticleForm(initial={'stags': tags},
                           instance=self.object)
        return form

    def post(self, request, pk):
        self.object = get_object_or_404(Article, id=pk)
        article = ArticleForm(request.POST, instance=self.object)
        tags = request.POST.get('stags', None)
        if article.is_valid():
            model_instance = article.save()
        model_instance.tags.clear()

        if tags:
            for tag in tags.split():
                try:
                    tag_record = Tag.objects.get(name=tag)
                except Exception:
                    tag_record = Tag.objects.create(name=tag)
                model_instance.tags.add(tag_record)


        return redirect(reverse('article_detail', args=[pk]))


class ArticleCreateView(CreateView):
    model = Article
    template_name_suffix = '_create'
    fields = []

    def get_context_data(self, **kwargs):
        context = super(ArticleCreateView, self).get_context_data(
            **kwargs)
        form = ArticleForm()
        context['form'] = form
        return context

    def post(self, request):
        article = ArticleForm(request.POST)
        article_instance = article.save(commit=False)
        article_instance.save()
        tags = request.POST.get('stags', None)
        if tags:
            for tag in tags.split():
                tag_record = Tag.objects.filter(name=tag)
                if not tag_record:
                    tag_record = Tag.objects.create(name=tag)
                article_instance.tags.add(tag_record)
        return redirect(reverse('article_detail', args=[article_instance.id]))


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(
            **kwargs)
        tags = self.object.tags.all()
        context['article_tags'] = tags
        return context

    def post(self, request, pk):
        self.object = get_object_or_404(Article, id=pk)
        comment = CommentForm(request.POST)
        commit_instance = comment.save()
        self.object.comments.add(commit_instance)
        self.object.save()
        return redirect(reverse('article_detail', args=[pk]))


class ArticleListView(ListView):
    model = Article
    tag_id = None

    def get_queryset(self):
        if self.tag_id:
            tag = get_object_or_404(Tag, id = self.tag_id)
            return tag.article_set.all()
        return super(ArticleListView, self).get_queryset()
