from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    blank=True)
    content = models.CharField(max_length=10000)
