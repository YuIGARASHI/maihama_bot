import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.train.train_info_handler import TrainInfoHandler
from src.tweet.tweet_handler import TweetHandler

if __name__ == "__main__":
    train_info_handler = TrainInfoHandler()
    tweet_handler = TweetHandler()

    status_summary, status_detail = train_info_handler.get_keiyo_line_info()
    # ステータス更新
    train_info_handler.check_and_update_state(status_detail)
    tweet_str = train_info_handler.make_tweet_str(status_detail)
    tweet_handler.post_tweet(tweet_str)