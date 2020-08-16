import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.tweet.tweet_handler import TweetHandler
from src.news_release.news_release_handler import NewsReleaseHandler

if __name__ == "__main__":
    news_release_handler = NewsReleaseHandler()
    tweet_handler = TweetHandler()

    news_release_text, news_release_link = news_release_handler.fetch_news_release()
    if news_release_handler.check_and_update_state(news_release_text):
        tweet_str = news_release_handler.make_tweet_str(news_release_text, news_release_link)
        tweet_handler.post_tweet(tweet_str)