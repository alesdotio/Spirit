# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from spirit.topic.models import Topic


class TopicTag(models.Model):
    slug = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.slug


class TopicTagRelation(models.Model):
    topic = models.ForeignKey(Topic, related_name='topictagrelation_set')
    tag = models.ForeignKey(TopicTag, related_name='topictagrelation_set')
    date_created = models.DateTimeField(auto_now_add=True)
