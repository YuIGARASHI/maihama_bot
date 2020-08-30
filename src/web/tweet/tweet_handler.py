import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.web.util.api_key_handler import ApiKeyHandler
import tweepy
import datetime


class TweetObj:
    def __init__(self, tweet):
        self.text = tweet.text
        self.retweet_count = tweet.retweet_count   # リツイート回数
        self.favorite_count = tweet.favorite_count # いいね回数
        # tweet作成時間。UTCから日本時間に変換する。
        created_at_utc_dt = tweet.created_at
        created_at_jp_dt = created_at_utc_dt + datetime.timedelta(hours=9)
        self.created_at = created_at_jp_dt.strftime('%m月%d日 %H:%M') # => 08月30日 15:54

    def print_myself(self):
        print("=====Tweet Object=====")
        print("ツイート：" + self.text)
        print("リツイート回数：" + str(self.retweet_count))
        print("いいね回数：" + str(self.favorite_count))
        print("ツイート時刻：" + self.created_at)

class TweetHandler():
    def __init__(self):
        api_key_handler = ApiKeyHandler()
        api_key, api_secret_key, access_token, secret_access_token = api_key_handler.get_twitter_api_keys()
        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, secret_access_token)
        self.api = tweepy.API(auth)

    def post_tweet(self, tweet_str):
        self.api.update_status(tweet_str)

    def post_tweet_with_img(self, tweet_str, image_path):
        self.api.update_with_media(status=tweet_str, filename=image_path)

    def fetch_tweets(self, target_word, num_of_tweets):
        '''指定した語を含むツイートを、最新からさかのぼって指定した個数だけ取得する。

        ただしリツイートは取得しない。
        '''
        target_word += " -filter:retweets" # リツイートは取得しない
        tweet_list = []
        for tweet in tweepy.Cursor(self.api.search, q=target_word).items(num_of_tweets):
            tweet_list.append(TweetObj(tweet))
        return tweet_list

if __name__ == "__main__":
    tweet_handler = TweetHandler()
    # tweet_handler.post_tweet("サンプルツイート")
    tweet_list = tweet_handler.fetch_tweets("ディズニー", 10)
    for tweet in tweet_list:
        tweet.print_myself()
