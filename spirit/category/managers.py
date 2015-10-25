# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import Group

from django.db import models
from django.db.models import Q


class CategoryQuerySet(models.QuerySet):

    def unremoved(self):
        return self.filter(Q(parent=None) | Q(parent__is_removed=False),
                           is_removed=False)

    def public(self):
        return self.filter(is_private=False)

    def visible(self, user=None):
        return self.unremoved().public().can_access(user)

    def can_access(self, user=None):
        if user and user.is_authenticated():
            if getattr(user, 'st', None) and user.st.is_administrator:
                return self.all()
            groups = user.groups.all()
        else:
            groups = Group.objects.none()
        return self.filter(
            Q(restrict_access=None) |
            Q(restrict_access__contains=groups)
        )

    def can_topic(self, user):
        return self.filter(
            Q(restrict_topic=None) |
            Q(restrict_topic__contains=user.groups.all())
        )

    def can_comment(self, user):
        return self.filter(
            Q(restrict_comment=None) |
            Q(restrict_comment__contains=user.groups.all())
        )

    def opened(self):
        return self.filter(Q(parent=None) | Q(parent__is_closed=False),
                           is_closed=False)

    def parents(self):
        return self.filter(parent=None)

    def children(self, parent):
        if parent.is_subcategory:
            return self.none()

        return self.filter(parent=parent)
