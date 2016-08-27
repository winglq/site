from articles.models import Article
from django import template


register = template.Library()
@register.inclusion_tag('partial_article_list.html')
def show_article_list(object_list=None):
    if object_list:
        return {'object_list': object_list}
    return {'object_list': Article.objects.all()}

