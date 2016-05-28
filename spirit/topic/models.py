# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import timezone
from django.db.models import F
from django.utils.encoding import python_2_unicode_compatible

from .managers import TopicQuerySet
from ..core.utils.models import AutoSlugField


@python_2_unicode_compatible
class Topic(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='st_topics')
    category = models.ForeignKey('spirit_category.Category', verbose_name=_("category"))

    title = models.CharField(_("title"), max_length=255)
    slug = AutoSlugField(populate_from="title", db_index=False, blank=True)
    date = models.DateTimeField(_("date"), default=timezone.now)
    last_active = models.DateTimeField(_("last active"), default=timezone.now)
    last_commenter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='st_topics_last', null=True, blank=True, on_delete=models.SET_NULL)

    is_pinned = models.BooleanField(_("pinned"), default=False)
    is_globally_pinned = models.BooleanField(_("globally pinned"), default=False)
    is_closed = models.BooleanField(_("closed"), default=False)
    is_removed = models.BooleanField(default=False)

    view_count = models.PositiveIntegerField(_("views count"), default=0)
    comment_count = models.PositiveIntegerField(_("comment count"), default=0)

    objects = TopicQuerySet.as_manager()

    class Meta:
        ordering = ['-last_active', '-pk']
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    def __str__(self):
        return "%s" % self.title

    def get_absolute_url(self):
        if self.category_id == settings.ST_TOPIC_PRIVATE_CATEGORY_PK:
            return reverse('spirit:topic:private:detail', kwargs={'topic_id': str(self.id), 'slug': self.slug})
        else:
            return reverse('spirit:topic:detail', kwargs={'pk': str(self.id), 'slug': self.slug})

    def get_bookmark_url(self):
        if not self.is_visited:
            return self.get_absolute_url()

        if not self.has_new_comments:
            return self.bookmark.get_absolute_url()

        return self.bookmark.get_new_comment_url()

    @property
    def main_category(self):
        return self.category.parent or self.category

    @property
    def bookmark(self):
        # *bookmarks* is dynamically created by manager.with_bookmarks()
        try:
            assert len(self.bookmarks) <= 1, "Panic, too many bookmarks"
            return self.bookmarks[0]
        except (AttributeError, IndexError):
            return

    @property
    def new_comments_count(self):
        # This may not be accurate since bookmarks requires JS,
        # without JS only the first comment in a page is marked,
        # so this counter should be shown running a JS script
        if not self.bookmark:
            return 0

        # Comments may have been moved
        return max(0, self.comment_count - self.bookmarks[0].comment_number)

    @property
    def has_new_comments(self):
        return self.new_comments_count > 0

    @property
    def is_visited(self):
        return bool(self.bookmark)

    def increase_view_count(self):
        Topic.objects\
            .filter(pk=self.pk)\
            .update(view_count=F('view_count') + 1)

    def increase_comment_count(self):
        self.update_last_commenter()
        Topic.objects\
            .filter(pk=self.pk)\
            .update(comment_count=F('comment_count') + 1, last_active=timezone.now())

    def decrease_comment_count(self):
        # todo: update last_active to last() comment
        self.update_last_commenter()
        Topic.objects\
            .filter(pk=self.pk)\
            .update(comment_count=F('comment_count') - 1)

    def update_last_commenter(self):
        last_comment = self.comment_set.filter(is_removed=False).first()
        if last_comment and last_comment.user != self.last_commenter:
            self.last_commenter = last_comment.user
            self.save()

    def set_can_comment_attr(self, user):
        group_ids = user.groups.all().values_list('id', flat=True)
        setattr(self, 'can_comment', True)
        if self.category.restrict_comment.exists():
            setattr(self, 'can_comment', self.category.restrict_comment.through.objects.filter(
                category_id=self.category_id, group_id__in=group_ids).exists())


def increase_user_profile_comment_count(sender, instance, created, **kwargs):
    if created and not instance.category.is_private:
        instance.user.st.increase_topic_count()

post_save.connect(increase_user_profile_comment_count, sender=Topic, dispatch_uid='Topic:increase_user_profile_comment_count')


def decrease_user_profile_comment_count(sender, instance, **kwargs):
    if not instance.category.is_private:
        instance.user.st.decrease_topic_count()

post_delete.connect(decrease_user_profile_comment_count, sender=Topic, dispatch_uid='Topic:decrease_user_profile_comment_count')

