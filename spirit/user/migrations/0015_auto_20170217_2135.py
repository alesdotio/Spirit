# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0014_auto_20170217_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='last_seen',
            field=models.DateTimeField(auto_now_add=True, verbose_name='last seen'),
        ),
    ]
