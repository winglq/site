# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 09:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admineditor', '0002_auto_20160723_0901'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeArticle',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admineditor.Article')),
            ],
        ),
    ]
