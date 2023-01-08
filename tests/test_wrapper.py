from base64 import b64encode
import twpy.wrapper

from rich import print

if __name__ == '__main__':
    wrapper = twpy.wrapper.Wrapper()
    # resp = wrapper.rate_limit_status()
    # resp = wrapper.update(f'Web3イベントは可愛い子が多いので敷居が高くなっていると思います。活動頑張ってください！')
    # resp = wrapper.destroy(resp['id'])
    # resp = wrapper.media(open('hoge.jpg', 'rb'))
    # resp = wrapper.verify_credentials()
    # resp = wrapper.tweet_lookup()
    # resp = wrapper.user_tweet_timeline_by_id('1142625173524238336')
    # resp = wrapper.user_by_id(['1142625173524238336', '1394158690341556224'])
    # resp = wrapper.recent_research('ビットコイン')
    # resp = wrapper.following('1142625173524238336')
    with open('blank.png', "rb") as image_file:
        data = b64encode(image_file.read())
    resp = wrapper.update_profile_image(data)
    print(resp)

