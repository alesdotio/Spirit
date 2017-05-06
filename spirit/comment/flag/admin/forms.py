# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms

from django.utils.translation import ugettext_lazy as _

from ..models import CommentFlag


class CommentFlagForm(forms.ModelForm):
    is_closed = forms.BooleanField(required=False, label=_('Close this report'))

    class Meta:
        model = CommentFlag
        fields = ("is_closed", )

    def __init__(self, user=None, *args, **kwargs):
        super(CommentFlagForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        self.instance.moderator = self.user
        return super(CommentFlagForm, self).save(commit)
