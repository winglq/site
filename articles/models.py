from __future__ import unicode_literals

from django.db import models
from mysite.models import ModelHelper
from favor.models import Favorate
# Create your models here.
class Article(models.Model, ModelHelper):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    blank=True)
    content = models.CharField(max_length=10000)
    def __unicode__(self):
        return self.title
    _favor = models.ForeignKey("favor.Favorate", null=True)
    def get_favor(self):
        if self._favor is None:
            f = Favorate()
            f.save()
            self._favor = f
            self.save()
        return self._favor
    favor = property(get_favor)
