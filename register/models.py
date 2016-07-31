from __future__ import unicode_literals

from django.db import models

# Create your models here.
class RegisterMetadata(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    all_fields = models.CharField(max_length=2000)
    pub_date = models.DateTimeField('date created', auto_now_add=True)

    def __unicode__(self):
        return self.name

class RegisterURL(models.Model):
    uuid = models.UUIDField(primary_key=True)
    URL = models.URLField()
    metadata = models.OneToOneField(RegisterMetadata, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.URL

class RegisterResult(models.Model):
    id = models.AutoField(primary_key=True)
    regurl = models.ForeignKey('RegisterURL')
    results = models.TextField()
