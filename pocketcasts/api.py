# -*- coding: utf-8 -*-
"""TODO: Class description API"""
from episode import Episode
from podcast import Podcast
import requests


class Api(object):
    def __init__(self, email, password):
        self._session = requests.Session()
        formdata = {
            "user[email]": email,
            "user[password]": password,
            }
        response = self._session.post("https://play.pocketcasts.com"
                                      "/users/sign_in",
                                      data=formdata)
        response.raise_for_status()
        # TODO(Check if login was successful, code is 200 in every case)

    def my_podcasts(self):
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/podcasts/all.json")
        response.raise_for_status()

        podcasts = []
        for podcast_json in response.json()['podcasts']:
            podcast = Podcast._from_json(podcast_json, self)
            podcasts.append(podcast)
        return podcasts

    def featured_podcasts(self):
        response = self._session.get("https://static.pocketcasts.com"
                                     "/discover/json/featured.json")
        response.raise_for_status()

        podcasts = []
        for podcast_json in response.json()['result']['podcasts']:
            podcast = Podcast._from_json(podcast_json, self)
            podcasts.append(podcast)
        return podcasts

    def episodes_for_podcast(self, podcast_uuid,
                             sort_order=Podcast.SortOrder.NewestFirst):
        page = 1
        pages_left = True
        episodes = []
        podcast = self.podcast(podcast_uuid)
        while pages_left:
            params = {'page': page, 'sort': sort_order, 'uuid': podcast_uuid}
            response = self._session.post("https://play.pocketcasts.com"
                                          "/web/episodes/find_by_podcast.json",
                                          json=params)
            response.raise_for_status()

            json_response = response.json()
            for episode_json in json_response['result']['episodes']:
                episode = Episode._from_json(episode_json, podcast)
                # episode = episode_json
                episodes.append(episode)

            # we should never ever receive more episodes than specified
            # well, better be fault tolerant
            if(json_response['result']['total'] > len(episodes)):
                page = page + 1
            else:
                pages_left = False

        return episodes

    def podcast(self, uuid):
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/podcasts/podcast.json",
                                      json={'uuid': uuid})
        response.raise_for_status()
        response_json = response.json()
        podcast = Podcast._from_json(response_json['podcast'], self)

        return podcast

    def popular_podcasts(self):
        response = self._session.get("https://static.pocketcasts.com"
                                     "/discover/json/popular_world.json")
        response.raise_for_status()

        podcasts = []
        for podcast_json in response.json()['result']['podcasts']:
            podcast = Podcast._from_json(podcast_json, self)
            podcasts.append(podcast)
        return podcasts

    def trending_podcasts(self):
        response = self._session.get("https://static.pocketcasts.com"
                                     "/discover/json/trending.json")
        response.raise_for_status()

        podcasts = []
        for podcast_json in response.json()['result']['podcasts']:
            podcast = Podcast._from_json(podcast_json, self)
            podcasts.append(podcast)
        return podcasts

    def new_podcast_releases(self):
        response = self._session.post("https://play.pocketcasts.com"
                                      "/web/episodes/"
                                      "new_releases_episodes.json")
        response.raise_for_status()

        episodes = []
        podcasts = {}
        for episode_json in response.json()['episodes']:
            podcast_uuid = episode_json['podcast_uuid']
            if podcast_uuid not in podcasts:
                podcasts[podcast_uuid] = self.podcast(podcast_uuid)
            episode = Episode._from_json(episode_json, podcasts[podcast_uuid])
            episodes.append(episode)
        return episodes
