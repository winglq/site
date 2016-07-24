from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('', max_length=100, null=True)
    email = models.EmailField('', null=True)
    content = models.TextField('')
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    blank=True)
    article = models.ForeignKey('articles.Article')

