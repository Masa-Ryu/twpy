from rich import print

from twpy import methods, wrapper

if __name__ == '__main__':
    functions = methods.Methods()

    # functions.post_tweet('test post1')
    # functions.delete_all_likes()
    # functions.unfollow_all()
    functions.delete_all_tweets()
    functions.print_rate_limit()
