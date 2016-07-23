from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1000)
