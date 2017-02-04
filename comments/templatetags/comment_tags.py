from django import template
from comments.forms import CommentForm
from comments.models import Comment


register = template.Library()


@register.inclusion_tag('partial_comment_create.html')
def show_comment_create():
    form = CommentForm()
    return {'form': form}


@register.inclusion_tag('partial_comment_list.html')
def show_comment_list(article):
    comments = article.comments.all()
    return {'object_list': comments}


