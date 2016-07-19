from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from models import Article
# Register your models here.

class ArticleAdmin(SummernoteModelAdmin):
    pass
admin.site.register(Article, ArticleAdmin)
