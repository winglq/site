from django.shortcuts import render
from favor.models import Favorate
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

# Create your views here.

def increase_like_count(request, id):
    favor = get_object_or_404(Favorate, id=id)
    favor.like_count = favor.like_count + 1
    favor.order_count = favor.like_count - favor.dislike_count
    favor.save()
    return redirect(request.META['HTTP_REFERER'])

def increase_dislike_count(request, id):
    favor = get_object_or_404(Favorate, id=id)
    favor.dislike_count = favor.dislike_count + 1
    favor.order_count = favor.like_count - favor.dislike_count
    favor.save()
    return redirect(request.META['HTTP_REFERER'])
