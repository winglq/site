from __future__ import unicode_literals
from django.db import models
from home import models as hmodels

# Create your models here.

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    is_home = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    blank=True)
    content = models.TextField()

    def _update_home_model(self):
        if self.is_home:
            try:
                homearticle = list(hmodels.HomeArticle.objects.all())[-1]
                homearticle.article = self
            except Exception:
                homearticle = \
                    hmodels.HomeArticle.objects.create(article=self)
            homearticle.save()
            

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        self._update_home_model()

    def __unicode__(self):
        return self.title

