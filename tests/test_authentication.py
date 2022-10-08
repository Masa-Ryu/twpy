import twpy.authentication

from rich import print


def auth():
    print(resp1, resp2)


def post_tweet():
    url = "https://api.twitter.com/1.1/statuses/update.json"
    params = {"status": "Hello, World!"}
    req = resp1.post(url, params=params)
    if req.status_code == 200:
        print("OK")
        print(req.headers)
    else:
        print("Error: %d" % req.status_code)


if __name__ == '__main__':
    authentication = twpy.authentication.Authentication()
    resp1, resp2 = authentication.set_api()
    post_tweet()
