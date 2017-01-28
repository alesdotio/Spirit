# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_topic', '0004_update_last_commenter'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='reindex_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='reindex at'),
        ),
    ]
