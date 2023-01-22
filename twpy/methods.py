from datetime import datetime, timezone, timedelta

from rich import print

from twpy.wrapper import Wrapper


class Methods(Wrapper):
    def __init__(self, file_name=None, api_info=None, guest=False):
        super().__init__(file_name, api_info, guest)

    def delete_all_likes(self):
        favorites = self.favorites_list()
        if not favorites == []:
            for favorite in favorites:
                self.destroy_favorite(favorite.get('id_str'))

    def unfollow_all(self):
        following_list = self.following_ids()
        for following_id in following_list['ids']:
            self.unfollow(user_id=following_id)

    def delete_all_tweets(self):
        my_information = self.verify_credentials()
        my_id = my_information['id_str']
        next_token = None
        while True:
            tweets = self.user_tweet_timeline_by_id(my_id, next_token)
            if tweets.get('meta', {}).get('result_count') == 0:
                break

            for tweet in tweets['data']:
                if 'RT @' in tweet['text']:
                    self.unretweet(tweet_id=tweet['id'])
                else:
                    self.delete_tweet(tweet_id=tweet['id'])

            if tweets.get('meta', {}).get('next_token') is not None:
                next_token = tweets['meta'].get('next_token')
            else:
                break

    def delete_tweets_except_retweets(self):
        pass

    def delete_tweets_except_media(self):
        pass

    def delete_tweets_except_like(self):
        pass

    def delete_bookmark(self):
        pass

    def delete_list(self):
        pass

    def delete_block_user(self):
        pass

    def delete_mute_user(self):
        pass

    def print_rate_limit(self):
        rate_limits = self.rate_limit_status()
        rate_limits = rate_limits['resources']
        for rate_limit in rate_limits:
            for _ in rate_limits[rate_limit]:
                if not rate_limits[rate_limit][_]['limit'] == rate_limits[rate_limit][_]['remaining']:
                    print(rate_limit, _)
                    print(f"Reset time(unix):{rate_limits[rate_limit][_]['reset']}")

                    jst = timezone(timedelta(hours=+9), 'JST')
                    epoch = rate_limits[rate_limit][_]['reset']
                    dt = datetime.fromtimestamp(epoch).replace(
                        tzinfo=timezone.utc
                        ).astimezone(tz=jst)
                    print(dt.isoformat())
                    print(f"Limit: {rate_limits[rate_limit][_]['limit']}")
                    print(f"Remaining: {rate_limits[rate_limit][_]['remaining']}")
