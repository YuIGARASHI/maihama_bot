import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
from src.web.tweet.tweet_handler import TweetHandler
from src.web.train.train_info_handler import TrainInfoHandler

if __name__ == "__main__":
    train_info_handler = TrainInfoHandler()
    tweet_handler = TweetHandler()
    status_summary, status_detail = train_info_handler.get_keiyo_line_info()
    update_flag = train_info_handler.check_and_update_state(status_detail)
    if update_flag:
        tweet_str = train_info_handler.make_tweet_str(status_detail)
        tweet_handler.post_tweet(tweet_str)