# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0012_auto_20161114_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_suspended_until',
            field=models.DateField(help_text='If set, the account will be disabled until this date.', null=True, verbose_name='suspended until', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='suspension_reason',
            field=models.TextField(help_text='The reason for the suspension, visible to the user.', null=True, verbose_name='suspension reason', blank=True),
        ),
    ]
