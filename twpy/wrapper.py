from requests import request

from twpy.authentication import Authentication


class Wrapper:
    def __init__(self, file_name=None):
        if file_name is None:
            authentication = Authentication()
        else:
            authentication = Authentication(file_name)
        self._API, self._HEADERS = authentication.set_api()

        self._reset = 0
        self._remaining = 0
        self._limit = 0
        self._path = ''
        self._V1_URL = 'https://api.twitter.com/1.1/'
        self._V2_URL = 'https://api.twitter.com/2/'
        self._api_num = 0
        self._table_name = f'API{self._api_num}'

    # def _write_rate_limit(self, table_name, path, limit, remaining, reset):
    #     data = rate_limit.read_table(table_name)
    #     for d in data:
    #         if path in d:
    #             if time() - float(d[3]) > 0:
    #                 rate_limit.update_record(table_name, path, remaining, reset)
    #                 break
    #             else:
    #                 remaining = int(d[2]) - 1
    #                 reset = d[3]
    #                 rate_limit.update_record(table_name, path, remaining, reset)
    #                 break
    #     else:
    #         rate_limit.new_record(table_name, path, limit, remaining, reset)
    #     self._reset = 0
    #     self._remaining = 0
    #     self._limit = 0
    #     self._path = ''
    #
    # def _check_rate_limit(self, table_name, path):
    #     data = rate_limit.read_table(table_name)
    #     for d in data:
    #         if path in d:
    #             if d[2] <= 0:
    #                 if time() - float(d[3]) > 0:
    #                     return True
    #                 else:
    #                     return False
    #             else:
    #                 return True
    #     else:
    #         return True

    def _request(self, version, method, path, payload=None):
        # if self._check_rate_limit(self._table_name, self._path):
        if payload is None:
            payload = {}
        if version == 0:  # Todo: for media
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

        # if res.headers.get('x-rate-limit-limit') is None:
        #     self._limit = 300
        # else:
        #     self._limit = res.headers['x-rate-limit-limit']
        # if res.headers.get('x-rate-limit-remaining') is None:
        #     self._remaining = 299
        # else:
        #     self._remaining = res.headers['x-rate-limit-remaining']
        # if res.headers.get('x-rate-limit-reset') is None:
        #     self._reset = int(time()) + 10800
        # else:
        #     self._reset = res.headers['x-rate-limit-reset']
        # self._write_rate_limit(
        #         self._table_name, self._path, self._limit, self._remaining,
        #         self._reset
        #         )
        if res.status_code == 200:
            return res.json()
        else:
            raise ConnectionError(
                    f'Status code:{res.status_code}, Error message:{res.json()}'
                    )
        # else:
        #     if version == 2:
        #         print('Rate limit exceed!')
        #         # Todo: キューに入れるとか
        #     else:
        #         if self._api_num == 6:
        #             self._api_num = 0
        #         else:
        #             self._api_num += 1
        #         self._table_name = f'API{self._api_num}'
        #         print(f'Change API. Next API name is {self._table_name}')
        #         self._set_api(self._table_name)
        #         await self._request(version, method, path, payload)

    def rate_limit_status(self):
        version = 1
        path = 'application/rate_limit_status.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {

                }
        result = self._request(version, 'GET', path, payload)
        return result

    def verify_credentials(self):
        version = 1
        path = 'account/verify_credentials.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {

                }
        result = self._request(version, 'GET', path, payload)
        return result

    def update(self, text, media_ids=None):
        version = 1
        path = 'statuses/update.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {
                'status': text
                }
        if media_ids is not None:
            payload['media_ids'] = media_ids
        result = self._request(version, 'POST', path, payload)
        return result

    def destroy(self, tweet_id):
        version = 1
        path = f'statuses/destroy/{tweet_id}.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {

                }
        result = self._request(version, 'POST', path, payload)
        return result

    def retweet(self, tweet_id):
        version = 1
        path = f'statuses/retweet/{tweet_id}.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {

                }
        result = self._request(version, 'POST', path, payload)
        return result

    def unretweet(self, tweet_id):
        version = 1
        path = f'statuses/unretweet/{tweet_id}.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {

                }
        result = self._request(version, 'POST', path, payload)
        return result

    def media(self, media):
        version = 0
        path = 'https://upload.twitter.com/1.1/media/upload.json'
        self._path = 'media'
        payload = {
                'media': media
                }
        result = self._request(version, 'POST', path, payload)
        return result

    def tweet_lookup(self, tweet_ids):
        version = 1
        if type(tweet_ids) is list:
            if len(tweet_ids) > 100:
                raise ValueError('Too many ids')
            path = 'statuses/lookup.json'
            self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
            for _ in range(len(tweet_ids)):
                path += tweet_ids[_]
                if not _ == len(tweet_ids) - 1:
                    path += ','
            payload = {}
        else:
            path = 'statuses/show.json'
            self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
            payload = {}
        result = self._request(version, 'GET', path, payload)
        return result

    def get_retweets(self, tweet_ids):
        version = 1
        if type(tweet_ids) is list:
            if len(tweet_ids) > 100:
                raise ValueError('Too many ids')
            path = 'statuses/retweeters/ids.json'
            self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
            for _ in range(len(tweet_ids)):
                path += tweet_ids[_]
                if not _ == len(tweet_ids) - 1:
                    path += ','
            payload = {}
        else:
            path = f'statuses/retweets/{tweet_ids}.json'
            self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
            payload = {}
        result = self._request(version, 'GET', path, payload)
        return result

    def create_favorite(self, tweet_id):
        version = 1
        path = 'favorites/create.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {
                'id': tweet_id
                }
        result = self._request(version, 'POST', path, payload)
        return result

    def destroy_favorite(self, tweet_id):
        version = 1
        path = 'favorites/destroy.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {
                'id': tweet_id
                }
        result = self._request(version, 'POST', path, payload)
        return result

    def favorites_list(self):
        version = 1
        path = 'favorites/list.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {
                }
        result = self._request(version, 'GET', path, payload)
        return result

    def search(
            self, keyword, geocode=None, lang=None, locale=None, count=None,
            until=None, since_id=None, max_id=None, include_entities=None
            ):
        version = 1
        path = 'search/tweets.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
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
        result = self._request(version, 'GET', path, payload)
        return result

    def home_timeline(self):
        version = 1
        path = 'statuses/home_timeline.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {
                }
        result = self._request(version, 'GET', path, payload)
        return result

    def mentions_timeline(self):
        version = 1
        path = 'statuses/mentions_timeline.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {
                }
        result = self._request(version, 'GET', path, payload)
        return result

    def user_timeline(self):
        version = 1
        path = 'statuses/user_timeline.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {
                }
        result = self._request(version, 'GET', path, payload)
        return result

    def follow(self, screen_name=None, user_id=None):
        if screen_name is None and user_id is None:
            raise TypeError('Please input screen_name or user_id')
        else:
            if screen_name is not None and user_id is not None:
                screen_name = None
                version = 1
                path = 'friendships/create.json'
                self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
                payload = {
                        }
                if screen_name is not None:
                    payload['screen_name'] = screen_name
                if user_id is not None:
                    payload['user_id'] = user_id
                result = self._request(version, 'POST', path, payload)
                return result

    def unfollow(self, screen_name=None, user_id=None):
        if screen_name is None and user_id is None:
            raise TypeError('Please input screen_name or user_id')
        else:
            if screen_name is not None and user_id is not None:
                screen_name = None
            version = 1
            path = 'friendships/destroy.json'
            self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
            payload = {
                    }
            if screen_name is not None:
                payload['screen_name'] = screen_name
            if user_id is not None:
                payload['user_id'] = user_id
            result = self._request(version, 'POST', path, payload)
            return result

    def following_ids(self):
        version = 1
        path = 'friends/ids.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {
                }
        result = self._request(version, 'GET', path, payload)
        return result

    def followers_ids(self, screen_name=None, user_id=None):
        version = 1
        path = 'followers/ids.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {
                }
        result = self._request(version, 'GET', path, payload)
        return result

    def update_profile_image(self, image):
        version = 1
        path = 'account/update_profile_image.json'
        self._path = f'{path.split("/")[0]}-{path.split("/")[1].replace(".json", "")}'
        payload = {
                'image': image
                }
        result = self._request(version, 'POST', path, payload)
        return result

    def tweet_usercontext(self, id_):
        version = 2
        if type(id_) is list:
            if len(id_) > 100:
                raise ValueError('Too many ids')
            path = 'tweets?ids='
            self._path = 'tweet_lookup'
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
            self._path = 'tweet_lookup'
            payload = {}
        result = self._request(version, 'GET', path, payload)
        return result

    def user_by_id(self, id_):
        version = 2
        if type(id_) is list:
            if len(id_) > 100:
                raise ValueError('Too many ids')
            path = 'users?ids='
            self._path = 'user_lookup'
            for _ in range(len(id_)):
                path += id_[_]
                if not _ == len(id_) - 1:
                    path += ','
            payload = {}
        else:
            path = f'users/{id_}'
            self._path = 'user_lookup'
            payload = {
                    'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
                    }
        result = self._request(version, 'GET', path, payload)
        return result

    def user_by_username(self, username):
        version = 2
        if type(username) is list:
            if len(username) > 100:
                raise ValueError('Too many username')
            path = 'users/by?usernames='
            self._path = 'user_lookup'
            for _ in range(len(username)):
                path += username[_]
                if not _ == len(username) - 1:
                    path += ','
            payload = {}
        else:
            path = f'users/by/username/{username}'
            self._path = 'user_lookup'
            payload = {}
        result = self._request(version, 'GET', path, payload)
        return result

    def followers(self, id_):
        version = 2
        path = f'users/{id_}/followers'
        self._path = 'followers'
        payload = {
                'max_results':  1000,
                'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,public_metrics,organic_metrics,promoted_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
                'user.fields':  'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
                }
        result = self._request(version, 'GET', path, payload)
        return result

    def following(self, id_):
        version = 2
        path = f'users/{id_}/following'
        self._path = 'following'
        payload = {
                'max_results':  1000,
                'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,public_metrics,organic_metrics,promoted_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld',
                'user.fields':  'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
                }
        result = self._request(version, 'GET', path, payload)
        return result

    # def follow(self, id_, target_user_id):
    #     version = 1
    #     path = f'{self._V2_URL}users/{id_}/following'
    #     self._path = 'follow'
    #     payload = {
    #         'target_user_id': target_user_id
    #     }
    #     result = self._request(version, 'POST', path, payload)
    #     return result
    #
    # def unfollow(self, source_user_id, target_user_id):
    #     version = 1
    #     path = f'{self._V2_URL}users/{source_user_id}/following/{target_user_id}'
    #     self._path = 'unfollow'
    #     result = self._request(version, 'DELETE', path)
    #     return result
    #
    def block(self, id_, target_user_id):
        version = 2
        path = f'users/{id_}/blocking'
        self._path = 'block'
        payload = {
                'target_user_id': target_user_id
                }
        result = self._request(version, 'POST', path, payload)
        return result

    # def blocks_lookup(self, id_):
    #     version = 1
    #     path = f'{self._V2_URL}users/{id_}/blocking'
    #     self._path = 'block_lookup'
    #     result = self._request(version, 'GET', path)
    #     return result
    #
    # def unblock(self, source_user_id, target_user_id):
    #     version = 1
    #     path = f'{self._V2_URL}users/{source_user_id}/blocking/{target_user_id}'
    #     self._path = 'unblock'
    #     result = self._request(version, 'DELETE', path)
    #     return result
    #
    # def like(self, id_, tweet_id):
    #     version = 1
    #     path = f'{self._V2_URL}users/{id_}/likes'
    #     self._path = 'like'
    #     payload = {
    #         'tweet_id': tweet_id
    #     }
    #     result = self._request(version, 'POST', path, payload)
    #     return result
    #
    # def liked_tweets(self, id_):
    #     version = 2
    #     path = f'users/{id_}/liked_tweets'
    #     self._path = 'like_tweets'
    #     result = self._request(version, 'GET', path)
    #     return result

    def liking_users(self, id_):
        version = 2
        path = f'tweets/{id_}/liking_users'
        self._path = 'liking_users'
        result = self._request(version, 'GET', path)
        return result

    # def unlike(self, id_, tweet_id):
    #     version = 1
    #     path = f'users/{id_}/likes/{tweet_id}'
    #     self._path = 'unlike'
    #     payload = {
    #         'tweet_id': tweet_id
    #     }
    #     result = self._request(version, 'DELETE', path, payload)
    #     return result

    def user_tweet_timeline_by_id(self, id_):
        version = 2
        path = f'users/{id_}/tweets'
        self._path = 'timeline'
        # payload = {
        #     'expansions': 'attachments.media_keys',
        #     'exclude': 'retweets,replies',
        #     'max_results': 100
        # 'media.fields': 'duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,non_public_metrics,organic_metrics,promoted_metrics',#url,
        # 'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,organic_metrics,possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,reply_settings,source,text,withheld'#'source,text'
        # }
        payload = {
                "expansions":   'attachments.media_keys',
                'media.fields': 'preview_image_url,type,url',
                'tweet.fields': 'created_at,lang',
                'user.fields':  'description,id,name',
                'max_results':  100
                }
        result = self._request(version, 'GET', path, payload)
        return result

    def user_mention_timeline_by_id(self, id_):
        version = 2
        path = f'users/{id_}/mentions'
        self._path = 'mention'
        payload = {

                }
        result = self._request(version, 'GET', path, payload)
        return result

    def recent_research(self, query):
        version = 2
        path = f'tweets/search/recent?query={query}'
        self._path = 'recent_search'
        payload = {
                'tweet.fields': 'source,lang'
                }
        result = self._request(version, 'GET', path, payload)
        return result

    def full_archive_search(self, query):
        version = 2
        path = f'tweets/search/all?query={query}'
        self._path = 'full_search'
        payload = {
                'tweet.fields': 'source'
                }
        result = self._request(version, 'GET', path, payload)
        return result

    def stream(self):
        version = 2
        path = f'tweets/sample/stream'
        self._path = 'stream'
        payload = {

                }
        result = self._request(version, 'GET', path, payload)
        return result
