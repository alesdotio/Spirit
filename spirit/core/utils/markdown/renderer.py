# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import mistune

from django.conf import settings
from django.utils.html import escape
from django.utils.text import slugify


def sanitize_url(url):
    url = escape(url)  # & -> &amp; ...
    parts = url.split(':', 1)

    if len(parts) == 1:  # No protocol (relative url)
        return url

    if parts[0] in settings.ST_ALLOWED_URL_PROTOCOLS:
        return url

    return ''


class Renderer(mistune.Renderer):

    # <h1 id="Lel \" &gt;="" &lt;script&gt;alert(1)&lt;="" script&gt;&lt;h1"="">Lel \"&gt; &lt;script&gt;alert(1)&lt;/script&gt;&lt;h1</h1>

    # Override
    def header(self, text, level, raw=None):
        """Adds an id attribute to titles with the text. This way it can be used for linking within the comment."""
        return '<h%d id="%s">%s</h%d>\n' % (level, escape(slugify(text)), text, level)

    # Override
    def autolink(self, link, is_email=False):
        link = sanitize_url(link)
        text = link

        if is_email:
            link = 'mailto:%s' % link

        if self.options['no_follow']:
            return '<a rel="nofollow" href="%s">%s</a>' % (link, text)

        return '<a href="%s">%s</a>' % (link, text)

    # Override
    def link(self, link, title, text):
        link = sanitize_url(link)

        if not title:
            if self.options['no_follow']:
                return '<a rel="nofollow" href="%s">%s</a>' % (link, text)

            return '<a href="%s">%s</a>' % (link, text)

        title = escape(title)

        if self.options['no_follow']:
            return '<a rel="nofollow" href="%s" title="%s">%s</a>' % (link, title, text)

        return '<a href="%s" title="%s">%s</a>' % (link, title, text)

    # Override
    def image(self, src, title, text):
        src = sanitize_url(src)
        text = escape(text)

        if title:
            title = escape(title)
            html = '<img src="%s" alt="%s" title="%s"' % (src, text, title)
        else:
            html = '<img src="%s" alt="%s"' % (src, text)

        if self.options.get('use_xhtml'):
            return '%s />' % html

        return '%s>' % html

    def audio_link(self, link):
        link = sanitize_url(link)
        return '<audio controls><source src="{link}">' \
               '<a rel="nofollow" href="{link}">{link}</a></audio>\n'.format(link=link)

    def image_link(self, src, title, text):
        image = self.image(src, title, text)
        return '<p>{image}</p>\n'.format(image=image)

    def emoji(self, name_class, name_raw):
        # todo: add no-follow to links since we are going to need migration to fix emojis
        return '<i class="tw tw-{name_class}" title=":{name_raw}:"></i>'.format(
            name_class=name_class,
            name_raw=name_raw
        )

    def mention(self, username, url):
        return '<a class="comment-mention" rel="nofollow" href="{url}">@{username}</a>'.format(
            username=username,
            url=url
        )

    def video_link(self, link):
        link = sanitize_url(link)
        return '<video controls><source src="{link}">' \
               '<a rel="nofollow" href="{link}">{link}</a></video>\n'.format(link=link)

    def youtube(self, video_id, start_hours=None, start_minutes=None, start_seconds=None):
        timestamp = 0
        if start_hours:
            timestamp += int(start_hours.replace('h', '')) * 60 * 60
        if start_minutes:
            timestamp += int(start_minutes.replace('m', '')) * 60
        if start_seconds:
            timestamp += int(start_seconds.replace('s', ''))
        timestamp = ('&start=%s' % timestamp) if timestamp else ''
        return '<span class="video"><iframe src="https://www.youtube.com/embed/{video_id}?html5=1{timestamp}" ' \
               'allowfullscreen></iframe></span>\n'.format(video_id=video_id, timestamp=timestamp)

    def vimeo(self, video_id):
        return '<span class="video"><iframe src="https://player.vimeo.com/video/{video_id}" ' \
               'allowfullscreen></iframe></span>\n'.format(video_id=video_id)

    def gfycat(self, video_id):
        return '<span class="video"><iframe src="https://gfycat.com/ifr/{video_id}" ' \
               'frameborder="0" scrolling="no" allowfullscreen></iframe></span>\n'.format(video_id=video_id)

    def twitch_channel(self, channel):
        return '<span class="video"><iframe src="https://player.twitch.tv/?channel={channel}&autoplay=true" ' \
               'width="100%" height="400" frameborder="0" scrolling="no" allowfullscreen="false">' \
               '</iframe></span>\n'.format(channel=channel)

    def twitch_video(self, video_id):
        return '<span class="video"><iframe src="https://player.twitch.tv/?video=v{video_id}&autoplay=true" ' \
               'width="100%" height="400" frameborder="0" scrolling="no" allowfullscreen="false">' \
               '</iframe></span>\n'.format(video_id=video_id)

    def poll(self, name):
        return '<poll name={name}>\n'.format(name=name)

    def poll_raw(self, poll_txt):
        poll_txt = poll_txt.replace('\n', '<br>')
        return '<p>{poll}</p>\n'.format(poll=poll_txt)
