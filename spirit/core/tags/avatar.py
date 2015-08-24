# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import math
import hashlib

from django.utils.encoding import smart_text
from django.utils.http import urlencode, urlquote
from easy_thumbnails.files import get_thumbnailer

from .registry import register


@register.simple_tag()
def get_avatar_color(user):
    # returns 0-215
    return smart_text(int(215 * math.log10(user.pk)))


@register.simple_tag()
def get_gravatar_url(user, size, rating='g', default='identicon'):
    url = "https://www.gravatar.com/avatar/"
    hash = hashlib.md5(user.email.strip().lower().encode('utf-8')).hexdigest()
    data = urlencode([('d', urlquote(default)),
                      ('s', str(size)),
                      ('r', rating)])
    return "".join((url, hash, '?', data))


@register.simple_tag()
def get_avatar_url(user, size=100):
    if user.st.avatar_chosen == 'file' and user.st.avatar:
        thumbnailer = get_thumbnailer(user.st.avatar)
        thumb = thumbnailer.get_thumbnail({
            'crop': True,
            'upscale': True,
            'size': (size, size),
        })
        return thumb.url
    else:
        return get_gravatar_url(user, size)

