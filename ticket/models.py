from __future__ import unicode_literals

from django.db import models


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    ticket = models.UUIDField()
    ip = models.GenericIPAddressField()

