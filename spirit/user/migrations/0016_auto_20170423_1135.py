# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0015_auto_20170217_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='hide_last_seen',
            field=models.BooleanField(default=False, help_text='Check this if you want to always appear offline', verbose_name='hide last seen'),
        ),
    ]
