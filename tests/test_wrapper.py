from base64 import b64encode
from twpy import wrapper

from rich import print

if __name__ == '__main__':
    wrapper_ = wrapper.Wrapper()

    # version1
    resp = wrapper_.rate_limit_status()
    # resp = wrapper_.verify_credentials()
    # resp = wrapper_.post_tweet(f'Test post')
    # resp = wrapper_.delete_tweet(tweet_id='')
    # resp = wrapper_.retweet(tweet_id='')
    # resp = wrapper_.unretweet(tweet_id='')
    # resp = wrapper_.media(open('hoge.jpg', 'rb'))
    # resp = wrapper_.tweet_lookup(tweet_ids='')
    # resp = wrapper_.get_retweets(tweet_ids='1613534140678418432')
    # resp = wrapper_.create_favorite(tweet_id='')
    # resp = wrapper_.destroy_favorite(tweet_id='')
    # resp = wrapper_.favorites_list()
    # resp = wrapper_.search(keyword='')
    # resp = wrapper_.home_timeline()
    # resp = wrapper_.mentions_timeline()
    # resp = wrapper_.user_timeline()
    # resp = wrapper_.follow()
    # resp = wrapper_.unfollow()
    # resp = wrapper_.following_ids()
    # with open('blank.png', "rb") as image_file:
    #     data = b64encode(image_file.read())
    # resp = wrapper_.change_profile_image(data)

    # version2
    # 1144773017169301504
    # resp = wrapper_.tweet_user_context(id_='1611958314958741505')
    # resp = wrapper_.user_by_id(['1142625173524238336', '1394158690341556224'])
    # resp = wrapper_.user_by_username(username='')
    # resp = wrapper_.followers('1142625173524238336')
    # resp = wrapper_.following('1142625173524238336')
    # resp = wrapper_.follow_v2(target_user_id='1142625173524238336')
    # resp = wrapper_.unfollow_v2('1142625173524238336')
    # resp = wrapper_.block('1142625173524238336')
    # resp = wrapper_.blocks_lookup('1142625173524238336')
    # resp = wrapper_.unblock('1142625173524238336')
    # resp = wrapper_.like(tweet_id='')
    # resp = wrapper_.liked_tweets()
    # resp = wrapper_.destroy_like(tweet_id='')
    # resp = wrapper_.user_tweet_timeline_by_id('1142625173524238336')
    # resp = wrapper_.user_mention_timeline_by_id('1142625173524238336')
    # resp = wrapper_.recent_research('Twitter')
    # resp = wrapper_.full_archive_search('Twitter')
    # resp = wrapper_.stream()

    print(resp)
