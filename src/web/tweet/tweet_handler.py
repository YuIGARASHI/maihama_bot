import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.web.util.api_key_handler import ApiKeyHandler
import tweepy


class TweetHandler():
    def __init__(self):
        api_key_handler = ApiKeyHandler()
        api_key, api_secret_key, access_token, secret_access_token = api_key_handler.get_twitter_api_keys()
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.access_token = access_token
        self.secret_access_token = secret_access_token

    def post_tweet(self, tweet_str):
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret_key)
        auth.set_access_token(self.access_token, self.secret_access_token)
        api = tweepy.API(auth)
        api.update_status(tweet_str)


if __name__ == "__main__":
    tweet_handler = TweetHandler()
    tweet_handler.post_tweet("サンプルツイート")