# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text

from ..models import Category


class CategoryForm(forms.ModelForm):
    enable_restrict_access = forms.BooleanField(initial=False, required=False, label=_('Limit who can access'))
    enable_restrict_topic = forms.BooleanField(initial=False, required=False, label=_('Limit who can create topics'))
    enable_restrict_comment = forms.BooleanField(initial=False, required=False, label=_('Limit who can comment'))

    class Meta:
        model = Category
        fields = ("parent", "title", "description", "order", "is_global", "is_closed", "is_removed",
                  "enable_restrict_access", "restrict_access",
                  "enable_restrict_topic", "restrict_topic",
                  "enable_restrict_comment", "restrict_comment")
        widgets = {
            'restrict_access': forms.CheckboxSelectMultiple,
            'restrict_topic': forms.CheckboxSelectMultiple,
            'restrict_comment': forms.CheckboxSelectMultiple,
        }

    def __init__(self, user, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        queryset = Category.objects.visible(user).parents()

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
            self.fields['enable_restrict_access'].initial = self.instance.restrict_access.exists()
            self.fields['enable_restrict_topic'].initial = self.instance.restrict_topic.exists()
            self.fields['enable_restrict_comment'].initial = self.instance.restrict_comment.exists()

        self.fields['parent'] = forms.ModelChoiceField(queryset=queryset, required=False)
        self.fields['parent'].label_from_instance = lambda obj: smart_text(obj.title)

    def clean_parent(self):
        parent = self.cleaned_data["parent"]

        if self.instance.pk:
            has_childrens = self.instance.category_set.all().exists()

            if parent and has_childrens:
                raise forms.ValidationError(_("The category you are updating "
                                              "can not have a parent since it has childrens"))

        return parent

    def clean_color(self):
        color = self.cleaned_data["color"]

        if color and not re.match(r'^#[A-Fa-f0-9]{3}([A-Fa-f0-9]{3}){0,1}$', color):
            raise forms.ValidationError(_("The input is not a valid hex color."))
        return color
