from rich import print

from twpy import methods, wrapper

if __name__ == '__main__':
    functions = methods.Methods(file_name='api.json')

    # functions.post_tweet('test post1')
    # functions.delete_all_likes()
    # functions.unfollow_all()
    # functions.delete_all_tweets()
    functions.print_rate_limit()
