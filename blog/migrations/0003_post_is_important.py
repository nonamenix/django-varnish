# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150401_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_important',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
