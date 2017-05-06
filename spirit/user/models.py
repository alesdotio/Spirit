# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import timedelta

from django.db import models
from django.db.models import F
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.deconstruct import deconstructible
from django.utils import timezone
import hashlib
import datetime

from ..core.utils.models import AutoSlugField


AVATAR_CHOICES = getattr(settings, 'ST_AVATAR_CHOICES', (
    ('gravatar', _('gravatar.com')),
    ('file', _('uploaded file')),
))


@deconstructible
class UploadToHandler(object):

    def __init__(self, prefix, instance_attribute):
        self.prefix = prefix
        self.instance_attribute = instance_attribute

    def __call__(self, instance, filename):
        return u"%s/%s/%s.%s" % (
            self.prefix,
            getattr(instance, self.instance_attribute),
            hashlib.md5(filename.encode("utf-8")).hexdigest(),
            unicode(filename.replace('/', '').split('.')[-1:][0])[:4]
        )


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_("profile"), related_name='st')

    slug = AutoSlugField(populate_from="user.username", db_index=False, blank=True)
    location = models.CharField(_("location"), max_length=75, blank=True)
    last_seen = models.DateTimeField(_("last seen"), auto_now_add=True)
    hide_last_seen = models.BooleanField(_("hide last seen"), default=False, help_text=_('Check this if you want to always appear offline'))
    last_ip = models.GenericIPAddressField(_("last ip"), blank=True, null=True)
    timezone = models.CharField(_("time zone"), max_length=32, default='UTC')
    is_administrator = models.BooleanField(_('administrator status'), default=False)
    is_moderator = models.BooleanField(_('moderator status'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False,
                                      help_text=_('Designates whether the user has verified his '
                                                  'account by email or by other means. Un-select this '
                                                  'to let the user activate his account.'))
    title = models.CharField(_("title"), max_length=128, blank=True)
    avatar = models.ImageField(_("avatar"), blank=True, null=True, upload_to=UploadToHandler('avatars', 'pk'))
    avatar_chosen = models.CharField(_("use avatar from"), max_length=32, choices=AVATAR_CHOICES, default=AVATAR_CHOICES[0][0])
    avatar_cached_url = models.CharField(max_length=255, blank=True, null=True)
    avatar_flair = models.CharField(_("avatar flair"), max_length=128, blank=True)
    user_title = models.CharField(_("user title"), max_length=128, blank=True)  # the user can choose this title

    topic_count = models.PositiveIntegerField(_("topic count"), default=0)
    comment_count = models.PositiveIntegerField(_("comment count"), default=0)
    given_likes_count = models.PositiveIntegerField(_("given likes count"), default=0)
    received_likes_count = models.PositiveIntegerField(_("received likes count"), default=0)

    last_post_hash = models.CharField(_("last post hash"), max_length=32, blank=True)
    last_post_on = models.DateTimeField(_("last post on"), null=True, blank=True)

    last_username_change_date = models.DateTimeField(blank=True, null=True)
    is_suspended_until = models.DateTimeField(_('suspended until'), null=True, blank=True, help_text=_('If set, the account will be disabled until this date.'))
    suspension_reason = models.TextField(_('suspension reason'), null=True, blank=True, help_text=_('The reason for the suspension, visible to the user.'))

    class Meta:
        verbose_name = _("forum profile")
        verbose_name_plural = _("forum profiles")

    def __unicode__(self):
        return u"%s" % self.user

    def __str__(self):
        return "%s" % self.user

    def save(self, *args, **kwargs):
        if self.user.is_superuser:
            self.is_administrator = True

        if self.is_administrator:
            self.is_moderator = True

        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('spirit:user:detail', kwargs={'pk': self.user.pk, 'slug': self.slug})

    def can_change_username(self):
        return bool(self.last_username_change_date)

    @property
    def is_online(self):
        return self.last_seen > timezone.now() - datetime.timedelta(minutes=5)

    @property
    def is_suspended(self):
        if self.is_suspended_until and self.is_suspended_until > timezone.now().date():
            return True
        return False

    def increase_comment_count(self):
        UserProfile.objects.filter(pk=self.pk).update(comment_count=F('comment_count') + 1)

    def decrease_comment_count(self):
        UserProfile.objects.filter(pk=self.pk).update(comment_count=F('comment_count') - 1)

    def increase_topic_count(self):
        UserProfile.objects.filter(pk=self.pk).update(topic_count=F('topic_count') + 1)

    def decrease_topic_count(self):
        UserProfile.objects.filter(pk=self.pk).update(topic_count=F('topic_count') - 1)

    def increase_given_likes_count(self):
        UserProfile.objects.filter(pk=self.pk).update(given_likes_count=F('given_likes_count') + 1)

    def decrease_given_likes_count(self):
        UserProfile.objects.filter(pk=self.pk).update(given_likes_count=F('given_likes_count') - 1)

    def increase_received_likes_count(self):
        UserProfile.objects.filter(pk=self.pk).update(received_likes_count=F('received_likes_count') + 1)

    def decrease_received_likes_count(self):
        UserProfile.objects.filter(pk=self.pk).update(received_likes_count=F('received_likes_count') - 1)

    def update_post_hash(self, post_hash):
        assert self.pk

        # Let the DB do the hash
        # comparison for atomicity
        return bool(UserProfile.objects
                    .filter(pk=self.pk)
                    .exclude(
                        last_post_hash=post_hash,
                        last_post_on__gte=timezone.now() - timedelta(
                            minutes=settings.ST_DOUBLE_POST_THRESHOLD_MINUTES))
                    .update(
                        last_post_hash=post_hash,
                        last_post_on=timezone.now()))


class UserSuspensionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='suspensions')
    date_created = models.DateTimeField(auto_now_add=True)
    suspended_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    suspended_until = models.DateTimeField(null=True, blank=True)
    suspension_reason = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('-date_created', )

    def __unicode__(self):
        if self.suspended_until:
            return _('%(user)s was suspended by %(suspended_by)s until %(suspended_until)s') % {
                'user': self.user.username,
                'suspended_by': self.suspended_by.username,
                'suspended_until': self.suspended_until,
            }
        else:
            return _('%(user)s suspension was lifted by %(suspended_by)s') % {
                'user': self.user.username,
                'suspended_by': self.suspended_by.username,
            }
