# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField(verbose_name=b'Publication date')),
                ('content', models.TextField(max_length=10000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
