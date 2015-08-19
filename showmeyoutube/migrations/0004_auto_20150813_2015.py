# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showmeyoutube', '0003_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.TextField(default='gfdgd'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.TextField(default='fsffsdfs'),
            preserve_default=False,
        ),
    ]
