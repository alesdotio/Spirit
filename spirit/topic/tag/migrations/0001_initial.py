# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spirit_topic', '0004_update_last_commenter'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopicTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TopicTagRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('tag', models.ForeignKey(related_name='topictagrelation_set', to='spirit_topic_tag.TopicTag')),
                ('topic', models.ForeignKey(related_name='topictagrelation_set', to='spirit_topic.Topic')),
            ],
        ),
    ]
