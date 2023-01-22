from requests import request

from twpy.authentication import Authentication


class Wrapper:
    def __init__(self, file_name=None, api_info=None, guest=False):
        authentication = Authentication()
        if file_name is None and api_info is None:
            self._API, self._HEADERS = authentication.from_file_authentication('apis.json')
        elif file_name:
            self._API, self._HEADERS = authentication.from_file_authentication(file_name)
        else:
            self._API, self._HEADERS = authentication.from_non_file_authentication(guest, **api_info)

        self._V1_URL = 'https://api.twitter.com/1.1/'
        self._V2_URL = 'https://api.twitter.com/2/'

    def _request(self, version, method, path, payload=None):
        if payload is None:
            payload = {}
        if version == 0:  # for media
            res = self._API.post(url=path, files=payload)
        elif version == 1:
            url = self._V1_URL + path
            if method == 'GET':
                res = self._API.get(url=url, params=payload)
            elif method == 'POST':
                res = self._API.post(url=url, data=payload)
            elif method == 'PUT':
                res = self._API.put(url=url, data=payload)
            elif method == 'DELETE':
                res = self._API.delete(url=url, data=payload)
            else:
                raise TypeError(
                        'Method error! Choose "GET", "POST", "PUT" or "DELETE"'
                        )
        elif version == 2:
            url = self._V2_URL + path
            if method == 'POST' or method == 'PUT' or method == 'DELETE':
                res = request(
                        method, url, headers=self._HEADERS, data=payload
                        )
            elif method == 'GET':
                res = request(
                        method, url, headers=self._HEADERS, params=payload
                        )
            else:
                raise TypeError(
                        'Method error! "GET", "POST", "PUT", "DELETE"'
                        )
        else:
            raise TypeError('Version error! Choose 0 or 1 or 2')

        if res.status_code == 200:
            return res.json()
        else:
            raise ConnectionError(
                    f'Status code:{res.status_code}, Error message:{res.json()}'
                    )

    # Version1
    def rate_limit_status(self):
        version = 1
        path = 'application/rate_limit_status.json'
        payload = {}
        return self._request(version, 'GET', path, payload)

    def verify_credentials(self):
        version = 1
        path = 'account/verify_credentials.json'
        payload = {}
        return self._request(version, 'GET', path, payload)

    def post_tweet(self, text, media_ids=None):
        version = 1
        path = 'statuses/update.json'
        payload = {
                'status': text
                }
        if media_ids is not None:
            payload['media_ids'] = media_ids
        return self._request(version, 'POST', path, payload)

    def delete_tweet(self, tweet_id):
        version = 1
        path = f'statuses/destroy/{tweet_id}.json'
        payload = {}
        return self._request(version, 'POST', path, payload)

    def retweet(self, tweet_id):
        version = 1
        path = f'statuses/retweet/{tweet_id}.json'
        payload = {}
        return self._request(version, 'POST', path, payload)

    def unretweet(self, tweet_id):
        version = 1
        path = f'statuses/unretweet/{tweet_id}.json'
        payload = {}
        return self._request(version, 'POST', path, payload)

    def media(self, media):
        version = 0
        path = 'https://upload.twitter.com/1.1/media/upload.json'
        payload = {
                'media': media
                }
        return self._request(version, 'POST', path, payload)

    def tweet_lookup(self, tweet_ids):
        version = 1
        if type(tweet_ids) is list:
            if len(tweet_ids) > 100:
                raise ValueError('Too many ids')
            path = 'statuses/lookup.json'
            for _ in range(len(tweet_ids)):
                path += tweet_ids[_]
                if not _ == len(tweet_ids) - 1:
                    path += ','
            payload = {}
        else:
            path = 'statuses/show.json'
            payload = {}
        return self._request(version, 'GET', path, payload)

    def get_retweets(self, tweet_ids):
        version = 1
        if type(tweet_ids) is list:
            if len(tweet_ids) > 100:
                raise ValueError('Too many ids')
            path = 'statuses/retweeters/ids.json'
            for _ in range(len(tweet_ids)):
                path += tweet_ids[_]
                if not _ == len(tweet_ids) - 1:
                    path += ','
            payload = {}
        else:
            path = f'statuses/retweets/{tweet_ids}.json'
            payload = {}
        return self._request(version, 'GET', path, payload)

    def create_favorite(self, tweet_id):
        version = 1
        path = 'favorites/create.json'
        payload = {
                'id': tweet_id
                }
        return self._request(version, 'POST', path, payload)

    def destroy_favorite(self, tweet_id):
        version = 1
        path = 'favorites/destroy.json'
        payload = {
                'id': tweet_id
                }
        return self._request(version, 'POST', path, payload)

    def favorites_list(self):
        version = 1
        path = 'favorites/list.json'
        payload = {}
        return self._request(version, 'GET', path, payload)

    def search(
            self, keyword, geocode=None, lang=None, locale=None, count=None,
            until=None, since_id=None, max_id=None, include_entities=None
            ):
        version = 1
        path = 'search/tweets.json'
        payload = {
                'q': keyword
                }
        if geocode is not None:
            payload['geocode'] = geocode
        if lang is not None:
            payload['lang'] = lang
        if locale is not None:
            payload['locale'] = locale
        if count is not None:
            payload['count'] = count
        if until is not None:
            payload['until'] = until
        if since_id is not None:
            payload['since_id'] = since_id
        if max_id is not None:
            payload['max_id'] = max_id
        if include_entities is not None:
            payload['include_entities'] = include_entities
        return self._request(version, 'GET', path, payload)

    def home_timeline(self):
        version = 1
        path = 'statuses/home_timeline.json'
        payload = {}
        return self._request(version, 'GET', path, payload)

    def mentions_timeline(self):
        version = 1
        path = 'statuses/mentions_timeline.json'
        payload = {}
        return self._request(version, 'GET', path, payload)

    def user_timeline(self):
        version = 1
        path = 'statuses/user_timeline.json'
        payload = {}
        return self._request(version, 'GET', path, payload)

    def follow(self, screen_name=None, user_id=None):
        if screen_name is None and user_id is None:
            raise TypeError('Please input screen_name or user_id')
        else:
            if screen_name is not None and user_id is not None:
                # Priority to user id
                screen_name = None
            version = 1
            path = 'friendships/create.json'
            payload = {}
            if screen_name is not None:
                payload['screen_name'] = screen_name
            if user_id is not None:
                payload['user_id'] = user_id
            return self._request(version, 'POST', path, payload)

    def unfollow(self, screen_name=None, user_id=None):
        if screen_name is None and user_id is None:
            raise TypeError('Please input screen_name or user_id')
        else:
            if screen_name is not None and user_id is not None:
                # Priority to user id
                screen_name = None
            version = 1
            path = 'friendships/destroy.json'
            payload = {}
            if screen_name is not None:
                payload['screen_name'] = screen_name
            if user_id is not None:
                payload['user_id'] = user_id
            return self._request(version, 'POST', path, payload)

    def following_ids(self):
        version = 1
        path = 'friends/ids.json'
        payload = {}
        return self._request(version, 'GET', path, payload)

    def followers_ids(self, screen_name=None, user_id=None):
        version = 1
        path = 'followers/ids.json'
        payload = {}
        if screen_name is not None:
            payload['screen_name'] = screen_name
        if user_id is not None:
            payload['user_id'] = user_id
        return self._request(version, 'GET', path, payload)

    def change_profile_image(self, image):
        version = 1
        path = 'account/update_profile_image.json'
        payload = {
                'image': image
                }
        result = self._request(version, 'POST', path, payload)
        return result

    # Version2
    def tweet_user_context(self, id_):
        version = 2
        if type(id_) is list:
            if len(id_) > 100:
                raise ValueError('Too many ids')
            path = 'tweets?ids='
            for _ in range(len(id_)):
                path += id_[_]
                if not _ == len(id_) - 1:
                    path += ','
            payload = {
                    "expansions":   'author_id,attachments.media_keys',
                    'media.fields': 'preview_image_url,type',
                    'place.fields': 'country,country_code',
                    'tweet.fields': 'created_at,lang',
                    'user.fields':  'created_at,description,id,name'
                    }
            # payload = {
            #     'expansions': 'attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id, in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id',
            #     'tweet.fields': 'attachments,author_id,created_at,entities,geo,id,in_reply_to_user_id,lang,possibly_sensitive,referenced_tweets,source,text,withheld',
            # 'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,organic_metrics,possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,reply_settings,source,text,withheld',
            # 'media.fields': 'duration_ms,height,media_key,non_public_metrics,organic_metrics,preview_image_url,promoted_metrics,public_metrics,type,url,width'
            # }
        else:
            path = f'tweets/{id_}'
            payload = {}
        return self._request(version, 'GET', path, payload)

    def user_by_id(self, id_):
        version = 2
        if type(id_) is list:
            if len(id_) > 100:
                raise ValueError('Too many ids')
            path = 'users?ids='
            for _ in range(len(id_)):
                path += id_[_]
                if not _ == len(id_) - 1:
                    path += ','
            payload = {}
        else:
            path = f'users/{id_}'
            payload = {
                    'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
                    }
        return self._request(version, 'GET', path, payload)

    def user_by_username(self, username):
        version = 2
        if type(username) is list:
            if len(username) > 100:
                raise ValueError('Too many username')
            path = 'users/by?usernames='
            for _ in range(len(username)):
                path += username[_]
                if not _ == len(username) - 1:
                    path += ','
            payload = {}
        else:
            path = f'users/by/username/{username}'
            payload = {}
        return self._request(version, 'GET', path, payload)

    def followers(self, id_):
        version = 2
        path = f'users/{id_}/followers'
        payload = {
                'max_results':  1000,
                'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,public_metrics,organic_metrics,promoted_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
                'user.fields':  'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
                }
        return self._request(version, 'GET', path, payload)

    def following(self, id_):
        version = 2
        path = f'users/{id_}/following'
        payload = {
                'max_results':  1000,
                'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,public_metrics,organic_metrics,promoted_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
                'user.fields':  'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
                }
        return self._request(version, 'GET', path, payload)

    def follow_v2(self, id_, target_user_id):
        version = 2
        path = f'users/{id_}/following'
        payload = {
                'target_user_id': target_user_id
                }
        return self._request(version, 'POST', path, payload)

    def unfollow_v2(self, source_user_id, target_user_id):
        version = 2
        path = f'users/{source_user_id}/following/{target_user_id}'
        return self._request(version, 'DELETE', path)

    def block(self, id_, target_user_id):
        version = 2
        path = f'users/{id_}/blocking'
        payload = {
                'target_user_id': target_user_id
                }
        return self._request(version, 'POST', path, payload)

    def blocks_lookup(self, id_):
        version = 2
        path = f'users/{id_}/blocking'
        return self._request(version, 'GET', path)

    def unblock(self, source_user_id, target_user_id):
        version = 2
        path = f'users/{source_user_id}/blocking/{target_user_id}'
        return self._request(version, 'DELETE', path)

    def like(self, id_, tweet_id):
        version = 2
        path = f'users/{id_}/likes'
        payload = {
                'tweet_id': tweet_id
                }
        return self._request(version, 'POST', path, payload)

    def liked_tweets(self, id_):
        version = 2
        path = f'users/{id_}/liked_tweets'
        return self._request(version, 'GET', path)

    def liking_users(self, id_):
        version = 2
        path = f'tweets/{id_}/liking_users'
        return self._request(version, 'GET', path)

    def destroy_like(self, id_, tweet_id):
        version = 1
        path = f'users/{id_}/likes/{tweet_id}'
        payload = {
                'tweet_id': tweet_id
                }
        return self._request(version, 'DELETE', path, payload)

    def user_tweet_timeline_by_id(self, user_id, pagination_token=None):
        version = 2
        path = f'users/{user_id}/tweets'
        payload = {
                "expansions":   'attachments.media_keys',
                'media.fields': 'preview_image_url,type,url',
                'tweet.fields': 'created_at,lang',
                'user.fields':  'description,id,name',
                'max_results':  100
                }
        if pagination_token is not None:
            payload['pagination_token'] = pagination_token
        return self._request(version, 'GET', path, payload)

    def user_mention_timeline_by_id(self, id_):
        version = 2
        path = f'users/{id_}/mentions'
        payload = {}
        return self._request(version, 'GET', path, payload)

    def recent_research(self, query):
        version = 2
        path = f'tweets/search/recent?query={query}'
        payload = {
                'tweet.fields': 'source,lang'
                }
        return self._request(version, 'GET', path, payload)

    def full_archive_search(self, query):
        version = 2
        path = f'tweets/search/all?query={query}'
        payload = {
                'tweet.fields': 'source'
                }
        return self._request(version, 'GET', path, payload)

    def stream(self):
        version = 2
        path = f'tweets/sample/stream'
        payload = {}
        return self._request(version, 'GET', path, payload)
