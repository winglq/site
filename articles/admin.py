from django.contrib import admin
from models import Article
from django_summernote.admin import SummernoteModelAdmin

class ArticleAdmin(SummernoteModelAdmin):
    pass
admin.site.register(Article, ArticleAdmin)

# Register your models here.
