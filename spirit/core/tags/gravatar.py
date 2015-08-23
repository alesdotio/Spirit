# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import hashlib

from django.utils.http import urlencode, urlquote

from .registry import register


@register.simple_tag()
def get_gravatar_url(user, size, rating='g', default='identicon'):
    url = "https://www.gravatar.com/avatar/"
    hash = hashlib.md5(user.email.strip().lower().encode('utf-8')).hexdigest()
    data = urlencode([('d', urlquote(default)),
                      ('s', str(size)),
                      ('r', rating)])
    return "".join((url, hash, '?', data))


@register.simple_tag()
def get_avatar_url(user, size):
    if user.st.avatar_chosen == 'file' and user.st.avatar:
        return user.st.avatar.url  # TODO: thumbnails
    else:
        return get_gravatar_url(user, size)
