# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0004_auto_20150731_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='title',
            field=models.CharField(max_length=128, blank=True),
        ),
    ]
