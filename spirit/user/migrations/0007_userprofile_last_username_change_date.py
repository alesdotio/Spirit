# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0006_calculate_user_profile_stats'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_username_change_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
