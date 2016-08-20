from __future__ import unicode_literals

from django.db import models


class Ticket(models.Model):
    ticket = models.UUIDField(primary_key=True)
    ip = models.GenericIPAddressField()
    expired = models.BooleanField()

