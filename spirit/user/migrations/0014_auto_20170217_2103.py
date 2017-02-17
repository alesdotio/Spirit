# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0013_auto_20170212_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='avatar_cached_url',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
