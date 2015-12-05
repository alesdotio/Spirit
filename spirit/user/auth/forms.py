# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from ..forms import CleanEmailMixin

User = get_user_model()


class RegistrationForm(CleanEmailMixin, UserCreationForm):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput,
        help_text=_("To activate your account you will have to click the link we will send to this address."))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput, min_length=6,
        help_text=_("Please use a strong password: at least 6 characters long."))
    honeypot = forms.CharField(label=_("Leave blank"), required=False)

    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True  # Django model does not required this by default

    def clean_honeypot(self):
        """Check that nothing has been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]

        if value:
            raise forms.ValidationError(_("Do not fill this field."))

        return value

    def clean_username(self):
        username = self.cleaned_data["username"]

        if username.lower() in settings.ST_INVALID_USERNAMES:
            raise forms.ValidationError(_("The username is invalid."))

        if settings.ST_CASE_INSENSITIVE_EMAILS:
            is_taken = User.objects.filter(username__iexact=username).exists()
        else:
            is_taken = User.objects.filter(username__exact=username).exists()

        if is_taken:
            raise forms.ValidationError(_("The username is taken."))

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]

        if settings.ST_UNIQUE_EMAILS:
            if settings.ST_CASE_INSENSITIVE_EMAILS:
                is_taken = User._default_manager.filter(email__iexact=email).exists()
            else:
                is_taken = User._default_manager.filter(email__exact=email).exists()

            if is_taken:
                raise forms.ValidationError(_("A user with this email already exists."))

        return email

    def save(self, commit=True):
        self.instance.is_active = False
        return super(RegistrationForm, self).save(commit)


class LoginForm(AuthenticationForm):

    username = forms.CharField(label=_("Username or Email"), max_length=254)


class CustomPasswordResetForm(PasswordResetForm):

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.

        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.

        Allow users with unusable passwords to reset their password (for social login).
        """
        active_users = get_user_model()._default_manager.filter(
            email__iexact=email, is_active=True)
        return (u for u in active_users)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
        else:
            html_context = Context({
                'content': body
            })
            email_message.attach_alternative(content=render_to_string("spirit/_base_email.html", html_context), mimetype='text/html')

        email_message.send()


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New password"), widget=forms.PasswordInput, min_length=6)


class ResendActivationForm(forms.Form):

    email = forms.CharField(label=_("Email"), widget=forms.EmailInput, max_length=254)

    def clean_email(self):
        email = self.cleaned_data["email"]

        if settings.ST_CASE_INSENSITIVE_EMAILS:
            email = email.lower()

        is_existent = User.objects\
            .filter(email=email)\
            .exists()

        if not is_existent:
            raise forms.ValidationError(_("The provided email does not exists."))

        self.user = User.objects\
            .filter(email=email, st__is_verified=False)\
            .order_by('-pk')\
            .first()

        if not self.user:
            raise forms.ValidationError(_("This account is verified, try logging-in."))

        return email

    def get_user(self):
        return self.user
