# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.template import defaultfilters
from django.conf import settings

from ..core.utils.timezone import timezones
from .models import UserProfile

User = get_user_model()

username_max_length = User._meta.get_field('username').max_length

TIMEZONE_CHOICES = timezones()


class CleanEmailMixin(object):

    def clean_email(self):
        email = self.cleaned_data["email"]

        if settings.ST_CASE_INSENSITIVE_EMAILS:
            email = email.lower()

        if not settings.ST_UNIQUE_EMAILS:
            return email

        is_taken = User.objects\
            .filter(email=email)\
            .exists()

        if is_taken:
            raise forms.ValidationError(_("The email is taken."))

        return email

    def get_email(self):
        return self.cleaned_data["email"]


class EmailCheckForm(CleanEmailMixin, forms.Form):

    email = forms.CharField(label=_("Email"), widget=forms.EmailInput, max_length=254)


class EmailChangeForm(CleanEmailMixin, forms.Form):

    email = forms.CharField(label=_("Email"), widget=forms.EmailInput, max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)
        if not self.user.has_usable_password():
            self.fields.pop('password')

    def clean_password(self):
        password = self.cleaned_data["password"]

        if not self.user.check_password(password):
            raise forms.ValidationError(_("The provided password is incorrect."))

        return password


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name")


class UserProfileForm(forms.ModelForm):

    timezone = forms.ChoiceField(label=_("Time zone"), choices=TIMEZONE_CHOICES)

    class Meta:
        model = UserProfile
        fields = ("location", "timezone", "hide_last_seen")

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        now = timezone.localtime(timezone.now())
        self.fields['timezone'].help_text = _('Current time is: %(date)s %(time)s') % {
            'date': defaultfilters.date(now),
            'time': defaultfilters.time(now)
        }


class AvatarChangeForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ("avatar_chosen", "avatar")
        widgets = {
            'avatar_chosen': forms.RadioSelect
        }


class UsernameChangeForm(forms.Form):
    new_username = forms.CharField(label=_("New username"), max_length=username_max_length)
    password = forms.CharField(label=_("Current password"), widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UsernameChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.user.has_usable_password():
            raise forms.ValidationError(_('You do not have a password set. Please use the set password form on your profile before trying to change your username.'))
        if self.user.st.last_username_change_date:
            raise forms.ValidationError(_('Sorry, you cannot change your username again!'))

    def clean_new_username(self):
        username = self.cleaned_data["new_username"]

        if username.lower() in settings.ST_INVALID_USERNAMES:
            raise forms.ValidationError(_("The username is invalid."))

        if settings.ST_CASE_INSENSITIVE_EMAILS:
            is_taken = User.objects.filter(username__iexact=username).exists()
        else:
            is_taken = User.objects.filter(username__exact=username).exists()

        if is_taken:
            raise forms.ValidationError(_("The username is taken."))

        return username

    def clean_password(self):
        password = self.cleaned_data["password"]

        if not self.user.check_password(password):
            raise forms.ValidationError(_("The provided password is incorrect."))

        return password
