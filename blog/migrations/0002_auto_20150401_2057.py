# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-datetime',)},
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 4, 1, 20, 57, 15, 56510), max_length=255),
            preserve_default=False,
        ),
    ]
