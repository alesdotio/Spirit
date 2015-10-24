# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_category', '0002_auto_fork_20150812_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_global',
            field=models.BooleanField(default=True, help_text='Designates whether the topics will bedisplayed in the all-categories list.', verbose_name='global'),
        ),
    ]
