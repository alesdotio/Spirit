# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0016_auto_20170423_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_flair',
            field=models.CharField(max_length=128, verbose_name='avatar flair', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_title',
            field=models.CharField(max_length=128, verbose_name='user title', blank=True),
        ),
    ]
