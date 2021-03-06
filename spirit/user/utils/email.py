# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from smtplib import SMTPException

from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template import Context
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string
from django.conf import settings

from .tokens import UserActivationTokenGenerator, UserEmailChangeTokenGenerator

logger = logging.getLogger('django')


def sender(request, subject, template_name, context, to):
    site = get_current_site(request)
    context.update({
        'site_name': site.name,
        'domain': site.domain,
        'protocol': 'https' if request.is_secure() else 'http'
    })
    message = render_to_string(template_name, context)
    html_context = Context({
        'content': message
    })

    for recipient in to:
        email = EmailMultiAlternatives(subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[recipient])
        email.attach_alternative(content=render_to_string("spirit/_base_email.html", html_context), mimetype="text/html")
        try:
            email.send()
        except (SMTPException, OSError) as err:
            logger.exception(err)


def send_activation_email(request, user):
    subject = _("User activation")
    template_name = 'spirit/user/activation_email.html'
    token = UserActivationTokenGenerator().generate(user)
    context = {'user_id': user.pk, 'token': token}
    sender(request, subject, template_name, context, [user.email, ])


def send_email_change_email(request, user, new_email):
    subject = _("Email change")
    template_name = 'spirit/user/email_change_email.html'
    token = UserEmailChangeTokenGenerator().generate(user, new_email)
    context = {'token': token, }
    # user might not have an email if using social auth
    send_to_email = user.email if user.email else new_email
    sender(request, subject, template_name, context, [send_to_email, ])


def send_notification_email(request, topic_notifications, comment):
    # TODO: test, implement
    subject = _("New notification: %(topic_name)s" % {'topic_name': comment.topic.title, })
    template_name = 'spirit/user/notification_email.html'
    context = {'comment': comment, }
    to = [tn.user.email
          for tn in topic_notifications
          if tn.user.is_subscribed]
    sender(request, subject, template_name, context, to)
