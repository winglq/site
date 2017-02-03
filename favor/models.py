from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Favorate(models.Model):
    id = models.AutoField(primary_key=True)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    order_count = models.IntegerField(
        default=0)
