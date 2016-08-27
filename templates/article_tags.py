from models import Article
from django import import template

register = template.Library()

@register.inclusion_tag('partial_article_list.html')
def show_article_list():
    object_list = Article.objects.all()
    return {'object_list': object_list}
