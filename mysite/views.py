from tags.models import Tag
from django.shortcuts import render
from django.views.generic import ListView as ListViewBase
from django.views.generic import DetailView as DetailViewBase
from django.views.generic.edit import FormView as FormViewBase
from django.views.generic.base import TemplateView as TemplateViewBase
from django.views.generic.base import View as DjangoViewBase


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


class TagWrapper(object):
    def __call__(self, cls):
        def get_context_data(inst, **kwargs):
            context = super(cls, inst).get_context_data(
                **kwargs)
            tags = Tag.objects.all()
            context['tags'] = \
                sorted(list(tags)[-10:],
                       key=lambda x : len(x.articles.all()),
                       reverse=True)
            return context

        cls.get_context_data = get_context_data
        return cls


@TagWrapper()
class ListView(ListViewBase):
    pass


@TagWrapper()
class DetailView(DetailViewBase):
    pass


@TagWrapper()
class FormView(FormViewBase):
    pass


@TagWrapper()
class TemplateView(TemplateViewBase):
    pass

class PageNotFindView(TemplateView):
    template_name = '404.html'

    def get(self, *args, **kwargs):
        response = super(PageNotFindView, self).get(*args, **kwargs)
        response.status_code = 404
        return response


class InternalErrorView(TemplateView):
    template_name = '500.html'

    def get(self, *args, **kwargs):
        response = super(PageNotFindView, self).get(*args, **kwargs)
        response.status_code = 500
        return response

handler404 = PageNotFindView.as_view()
handler500 = InternalErrorView.as_view()
