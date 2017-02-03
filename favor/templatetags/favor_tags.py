from django import template
from django.shortcuts import get_object_or_404
from favor.models import Favorate


register = template.Library()


@register.inclusion_tag('partial_favor_detail.html')
def show_favor(favor):
    return {'obj': favor}
