# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import spirit.user.models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0004_auto_fork_20150823_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(upload_to=spirit.user.models.UploadToHandler('avatars', 'pk'), null=True, verbose_name='avatar', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar_chosen',
            field=models.CharField(default='gravatar', max_length=32, verbose_name='use avatar from', choices=[('gravatar', 'gravatar.com'), ('file', 'uploaded file')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='title',
            field=models.CharField(max_length=128, verbose_name='title', blank=True),
        ),
    ]
