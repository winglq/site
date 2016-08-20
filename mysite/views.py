from tags.models import Tag
from django.shortcuts import render
from django.views.generic import ListView as ListViewBase
from django.views.generic import DetailView as DetailViewBase
from django.views.generic.edit import FormView as FormViewBase

class ViewBase(object):
    def __init__(self):
        super(ViewBase, self).__init__()
        self._context={}

    @property
    def context(self):
        tags = Tag.objects.all()
        self._context['tags']=sorted(list(tags)[-10:], key=lambda x : len(x.articles.all()), reverse=True)
        return self._context

    def render(self, request, template, context, *args, **kwargs):
        context.update(self.context)
        return render(request, template, context)

class ListView(ListViewBase):
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        tags = Tag.objects.all()
        context['tags'] = sorted(list(tags)[-10:], key=lambda x : len(x.articles.all()), reverse=True)
        return context

class DetailView(DetailViewBase):
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        tags = Tag.objects.all()
        context['tags'] = sorted(list(tags)[-10:], key=lambda x : len(x.articles.all()), reverse=True)
        return context
       

class FormView(FormViewBase):
    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        tags = Tag.objects.all()
        context['tags'] = sorted(list(tags)[-10:], key=lambda x : len(x.articles.all()), reverse=True)
        return context

