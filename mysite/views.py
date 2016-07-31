from tags.models import Tag
from django.shortcuts import render
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


