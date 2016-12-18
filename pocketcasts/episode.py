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
        self._api = podcast._api
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
        self._notes = kwargs.pop('notes', None)

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

    @playing_status.setter
    def playing_status(self, playing_status):
        # XXX(if-else is not very elegant, maybe refactor)
        if playing_status == Episode.PlayingStatus.Played:
            self._api.mark_as_played(self, True)
        elif playing_status == Episode.PlayingStatus.Unplayed:
            self._api.mark_as_played(self, False)
        else:
            # Playing Status 0 (Playing) shall not be accepted here
            raise ValueError("Invalid playing status: " + str(playing_status))
        self._playing_status = playing_status
        self._played_up_to = 0

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

    @starred.setter
    def starred(self, starred):
        self._api.mark_as_starred(self, starred)
        self._starred = starred

    @property
    def is_video(self):
        return self._is_video

    @property
    def played_up_to(self):
        return self._played_up_to

    @played_up_to.setter
    def played_up_to(self, position):
        self._api.update_episode_position(self, position)
        self._played_up_to = position
        self._playing_status = Episode.PlayingStatus.Unplayed

    @property
    def size(self):
        return self._size

    @property
    def notes(self):
        if self._notes is None:
            self._notes = self._api.load_notes(self)
        return self._notes

    @classmethod
    def _from_json(cls, json, podcast=None):
        json = json.copy()
        uuid = json.pop('uuid')
        return cls(uuid, podcast, **json)
