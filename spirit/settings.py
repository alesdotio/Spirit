# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE
# YOU MAY EXTEND/OVERWRITE THE DEFAULT VALUES IN YOUR settings.py FILE

from __future__ import unicode_literals
import os

ST_TOPIC_PRIVATE_CATEGORY_PK = 1

ST_RATELIMIT_ENABLE = True
ST_RATELIMIT_CACHE_PREFIX = 'srl'
ST_RATELIMIT_CACHE = 'default'
ST_RATELIMIT_FOR_PUBLISH = '1/10s'
ST_RATELIMIT_FOR_AUTH = '5/5m'
ST_RATELIMIT_FOR_REGISTER = '2/10s'

ST_NOTIFICATIONS_PER_PAGE = 20

ST_COMMENT_MAX_LEN = 3000
ST_MENTIONS_PER_COMMENT = 30
ST_DOUBLE_POST_THRESHOLD_MINUTES = 30

ST_YT_PAGINATOR_PAGE_RANGE = 3

ST_SEARCH_QUERY_MIN_LEN = 3

ST_USER_LAST_SEEN_THRESHOLD_MINUTES = 1

ST_PRIVATE_FORUM = False

ST_ALLOWED_UPLOAD_IMAGE_FORMAT = ('jpeg', 'png', 'gif')
ST_ALLOWED_URL_PROTOCOLS = {
    'http', 'https', 'mailto', 'ftp', 'ftps',
    'git', 'svn', 'magnet', 'irc', 'ircs'}

ST_UNICODE_SLUGS = True

ST_UNIQUE_EMAILS = True
ST_CASE_INSENSITIVE_EMAILS = True

ST_BASE_DIR = os.path.dirname(__file__)

ST_INVALID_USERNAMES = []

ST_ALLOW_ONE_USERNAME_CHANGE = False

#
# Django & Spirit settings defined below...
#

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'spirit.core',
    'spirit.admin',
    'spirit.search',

    'spirit.user',
    'spirit.user.admin',
    'spirit.user.auth',

    'spirit.group',
    'spirit.group.admin',

    'spirit.category',
    'spirit.category.admin',

    'spirit.topic',
    'spirit.topic.admin',
    'spirit.topic.favorite',
    'spirit.topic.moderate',
    'spirit.topic.notification',
    'spirit.topic.poll',  # todo: remove in Spirit v0.5
    'spirit.topic.private',
    'spirit.topic.unread',

    'spirit.comment',
    'spirit.comment.bookmark',
    'spirit.comment.flag',
    'spirit.comment.flag.admin',
    'spirit.comment.history',
    'spirit.comment.like',
    'spirit.comment.poll',

    # 'spirit.core.tests'
]

# python manage.py createcachetable
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'spirit_cache',
    },
}

AUTHENTICATION_BACKENDS = [
    'spirit.user.auth.backends.UsernameAuthBackend',
    'spirit.user.auth.backends.EmailAuthBackend',
]

LOGIN_URL = 'spirit:user:auth:login'
LOGIN_REDIRECT_URL = 'spirit:user:update'

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'spirit.core.middleware.XForwardedForMiddleware',
    'spirit.user.middleware.TimezoneMiddleware',
    'spirit.user.middleware.LastIPMiddleware',
    'spirit.user.middleware.LastSeenMiddleware',
    'spirit.user.middleware.ActiveUserMiddleware',
    'spirit.core.middleware.PrivateForumMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


#
# Third-party apps settings defined below...
#

# django-djconfig

INSTALLED_APPS += [
    'djconfig',
]

MIDDLEWARE_CLASSES += [
    'djconfig.middleware.DjConfigMiddleware',
]

TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'djconfig.context_processors.config',
]

# django-haystack

INSTALLED_APPS += [
    'haystack',
]

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'search/whoosh_index'),
    },
}


# easy_thumbnails

INSTALLED_APPS += [
    'easy_thumbnails',
]
