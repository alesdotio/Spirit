# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_user', '0017_auto_20170424_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_suspended_until',
            field=models.DateTimeField(help_text='If set, the account will be disabled until this date.', null=True, verbose_name='suspended until', blank=True),
        ),
    ]
