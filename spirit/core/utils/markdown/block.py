# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import copy

import mistune

from .parsers.poll import PollParser


class BlockGrammar(mistune.BlockGrammar):

    # todo: remove all *_link
    #link_block = re.compile(
    #    r'^https?://[^\s]+'
    #    r'(?:\n+|$)'
    #)

    audio_link = re.compile(
        r'^https?://[^\s]+\.(mp3|ogg|wav)'
        r'(\?[^\s]+)?'
        r'(?:\n+|$)'
    )

    image_link = re.compile(
        r'^https?://[^\s]+/(?P<image_name>[^\s]+)\.'
        r'(?P<extension>png|jpg|jpeg|gif|bmp|tif|tiff)'
        r'(\?[^\s]+)?'
        r'(?:\n+|$)'
    )

    video_link = re.compile(
        r'^https?://[^\s]+\.(mov|mp4|webm|ogv)'
        r'(\?[^\s]+)?'
        r'(?:\n+|$)'
    )

    # Try to get the video ID. Works for URLs of the form:
    # * https://www.youtube.com/watch?v=Z0UISCEe52Y
    # * http://youtu.be/afyK1HSFfgw
    # * https://www.youtube.com/embed/vsF0K3Ou1v0
    #
    # Also works for timestamps:
    # * https://www.youtube.com/watch?v=Z0UISCEe52Y&t=1m30s
    # * https://www.youtube.com/watch?v=O1QQajfobPw&t=1h1m38s
    # * https://www.youtube.com/watch?v=O1QQajfobPw&feature=youtu.be&t=3698
    # * https://youtu.be/O1QQajfobPw?t=3698
    # * https://youtu.be/O1QQajfobPw?t=1h1m38s
    #
    youtube = re.compile(
        r'^https?://(www\.)?'
        r'(youtube\.com/watch\?v='
        r'|youtu\.be/'
        r'|youtube\.com/embed/)'
        r'(?P<id>[a-zA-Z0-9_\-]{11})'
        r'((&|\?)('
        r'|(t=(?P<start_hours>[0-9]{1,2}h)?(?P<start_minutes>[0-9]{1,4}m)?(?P<start_seconds>[0-9]{1,5}s?)?)'
        r'|([^&\s]+)'
        r')){,10}'
        r'(?:\n+|$)'
    )

    # Try to get the video ID. Works for URLs of the form:
    # * https://vimeo.com/11111111
    # * https://www.vimeo.com/11111111
    # * https://player.vimeo.com/video/11111111
    # * https://vimeo.com/channels/11111111
    # * https://vimeo.com/groups/name/videos/11111111
    # * https://vimeo.com/album/2222222/video/11111111
    # * https://vimeo.com/11111111?param=value
    vimeo = re.compile(
        r'^https?://(www\.|player\.)?'
        r'vimeo\.com/'
        r'(channels/'
        r'|groups/[^/]+/videos/'
        r'|album/(\d+)/video/'
        r'|video/)?'
        r'(?P<id>\d+)'
        r'(\?[^\s]+)?'
        r'(?:\n+|$)'
    )

    # Try to get the video ID. Works for URLs of the form:
    # * https://gfycat.com/videoid
    # * https://www.gfycat.com/videoid
    # * http://gfycat.com/videoid
    # * http://www.gfycat.com/videoid
    gfycat = re.compile(
        r'^https?://(www\.)?'
        r'gfycat\.com/'
        r'(?P<id>\w+)'
        r'(\?[^\s]+)?'
        r'(?:\n+|$)'
    )

    # Try to get the channel. Works for URLs of the form:
    # https://www.twitch.tv/lirik
    twitch_channel = re.compile(
        r'^https?://(www\.)?'
        r'twitch\.tv/'
        r'(?P<channel>\w+)'
    )

    # Try to get the video. Works for URLs of the form:
    # https://www.twitch.tv/videos/432540384
    twitch_video = re.compile(
        r'^https?://(www\.)?'
        r'twitch\.tv/videos/'
        r'(?P<video_id>\w+)'
    )

    # Capture polls:
    # [poll name=foo min=1 max=1 close=1d mode=default]
    # # Which opt you prefer?
    # 1. opt 1
    # 2. opt 2
    # [/poll]
    poll = re.compile(
        r'^(?:\[poll'
        r'((?:\s+name=(?P<name>[\w\-_]+))'
        r'(?:\s+min=(?P<min>\d+))?'
        r'(?:\s+max=(?P<max>\d+))?'
        r'(?:\s+close=(?P<close>\d+)d)?'
        r'(?:\s+mode=(?P<mode>(default|secret)))?'
        r'|(?P<invalid_params>[^\]]*))'
        r'\])\n'
        r'((?:#\s*(?P<title>[^\n]+\n))?'
        r'(?P<choices>(?:\d+\.\s*[^\n]+\n){2,})'
        r'|(?P<invalid_body>(?:[^\n]+\n)*))'
        r'(?:\[/poll\])'
    )


class BlockLexer(mistune.BlockLexer):

    default_rules = copy.copy(mistune.BlockLexer.default_rules)
    default_rules.insert(0, 'audio_link')
    default_rules.insert(0, 'image_link')
    default_rules.insert(0, 'video_link')
    default_rules.insert(0, 'youtube')
    default_rules.insert(0, 'vimeo')
    default_rules.insert(0, 'gfycat')
    default_rules.insert(0, 'twitch_channel')
    default_rules.insert(0, 'twitch_video')
    default_rules.insert(0, 'poll')

    def __init__(self, rules=None, **kwargs):
        if rules is None:
            rules = BlockGrammar()

        super(BlockLexer, self).__init__(rules=rules, **kwargs)

        self.polls = {
            'polls': [],
            'choices': []
        }

    def parse_audio_link(self, m):
        self.tokens.append({
            'type': 'audio_link',
            'link': m.group(0).strip()
        })

    def parse_image_link(self, m):
        link = m.group(0).strip()
        title = m.group('image_name').strip()
        self.tokens.append({
            'type': 'image_link',
            'src': link,
            'title': title,
            'text': title
        })

    def parse_video_link(self, m):
        self.tokens.append({
            'type': 'video_link',
            'link': m.group(0).strip()
        })

    def parse_youtube(self, m):
        self.tokens.append({
            'type': 'youtube',
            'video_id': m.group("id"),
            'start_hours': m.group("start_hours"),
            'start_minutes': m.group("start_minutes"),
            'start_seconds': m.group("start_seconds"),
        })

    def parse_vimeo(self, m):
        self.tokens.append({
            'type': 'vimeo',
            'video_id': m.group("id")
        })

    def parse_gfycat(self, m):
        self.tokens.append({
            'type': 'gfycat',
            'video_id': m.group("id")
        })

    def parse_twitch_channel(self, m):
        self.tokens.append({
            'type': 'twitch_channel',
            'channel': m.group("channel")
        })

    def parse_twitch_video(self, m):
        self.tokens.append({
            'type': 'twitch_video',
            'video_id': m.group("video_id")
        })

    def parse_poll(self, m):
        parser = PollParser(polls=self.polls, data=m.groupdict())

        if parser.is_valid():
            poll = parser.cleaned_data['poll']
            choices = parser.cleaned_data['choices']
            self.polls['polls'].append(poll)
            self.polls['choices'].extend(choices)
            self.tokens.append({
                'type': 'poll',
                'name': poll['name']
            })
        else:
            self.tokens.append({
                'type': 'poll',
                'raw': m.group(0)
            })
