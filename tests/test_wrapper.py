from base64 import b64encode
from twpy import wrapper

from rich import print

if __name__ == '__main__':
    wrapper_ = wrapper.Wrapper()
    # resp = wrapper_.rate_limit_status()
    # resp = wrapper_.update(f'Web3イベントは可愛い子が多いので敷居が高くなっていると思います。活動頑張ってください！')
    # resp = wrapper_.destroy(resp['id'])
    # resp = wrapper_.media(open('hoge.jpg', 'rb'))
    # resp = wrapper_.verify_credentials()
    # resp = wrapper_.tweet_lookup()
    # resp = wrapper_.user_tweet_timeline_by_id('1142625173524238336')
    # resp = wrapper_.user_by_id(['1142625173524238336', '1394158690341556224'])
    # resp = wrapper_.recent_research('ビットコイン')
    # resp = wrapper_.following('1142625173524238336')
    with open('blank.png', "rb") as image_file:
        data = b64encode(image_file.read())
    resp = wrapper_.update_profile_image(data)
    print(resp)

