# -*- coding: utf-8 -*-
"""TODO 2"""
from datetime import datetime


class Episode(object):
    class PlayingStatus(object):
        Playing = 0
        # haven't seen 1 yet
        Unplayed = 2
        Played = 3

    def __init__(self, uuid, podcast, **kwargs):
        self._podcast = podcast
        # I don't know what is_deleted means exactly, it seems always False
        # I don't know what id means, it is an unsigned int or null
        self._uuid = uuid
        self._title = kwargs.pop('title', '')
        self._url = kwargs.pop('url', '')
        self._playing_status = kwargs.pop('playing_status',
                                          Episode.PlayingStatus.Unplayed)
        self._file_type = kwargs.pop('file_type', '')
        self._published_at = datetime.strptime(kwargs.pop('published_at',
                                                          datetime.today()
                                                          ),
                                               "%Y-%m-%d %H:%M:%S")
        self._duration = kwargs.pop('duration', 0)
        self._starred = bool(kwargs.pop('starred', 0))
        self._is_video = kwargs.pop('is_video', '')
        self._played_up_to = kwargs.pop('played_up_to', 0)
        self._size = kwargs.pop('size', 0)

    def __repr__(self):
        return str(self.__dict__)

    @property
    def uuid(self):
        return self._uuid

    @property
    def title(self):
        return self._title

    @property
    def url(self):
        return self._url

    @property
    def playing_status(self):
        return self._playing_status

    @property
    def file_type(self):
        return self._file_type

    @property
    def published_at(self):
        return self._published_at

    @property
    def duration(self):
        return self._duration

    @property
    def starred(self):
        return self._starred

    @property
    def is_video(self):
        return self._is_video

    @property
    def played_up_to(self):
        return self._played_up_to

    @property
    def size(self):
        return self._size

    @classmethod
    def _from_json(cls, json, podcast=None):
        json = json.copy()
        uuid = json.pop('uuid')
        return cls(uuid, podcast, **json)
