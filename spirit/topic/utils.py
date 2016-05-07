# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from ..comment.bookmark.models import CommentBookmark
from .notification.models import TopicNotification
from .unread.models import TopicUnread


def topic_viewed(request, topic):
    # Todo test detail views
    user = request.user
    comment_number = CommentBookmark.page_to_comment_number(request.GET.get('page', 1))

    if user.is_authenticated():
        try:
            bookmark = CommentBookmark.objects.get(user=user, topic=topic)
            if bookmark.comment_number < comment_number:
                bookmark.comment_number = comment_number
                bookmark.save()
        except CommentBookmark.DoesNotExist:
            CommentBookmark.objects.update_or_create(
                user=user,
                topic=topic,
                defaults={
                    'comment_number': comment_number,
                }
            )
        TopicNotification.mark_as_read(user=user, topic=topic)
        TopicUnread.create_or_mark_as_read(user=user, topic=topic)

    topic.increase_view_count()
