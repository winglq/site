from __future__ import unicode_literals

from django.db import models

# Create your models here.
class HomeArticle(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey('admineditor.Article')
