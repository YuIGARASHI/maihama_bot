import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.util.message_handler import MessageHandler
from src.tweet.tweet_handler import TweetHandler
from src.util.time_util import TimeUtil

if __name__ == "__main__":
    current_time = TimeUtil.get_current_time_str().split()[1]
    available_times = ["08:", "12:", "16:", "20:"]
    post_flag = False
    for available_time in available_times:
        if available_time in current_time:
            post_flag = True
    if post_flag:
        message_handler = MessageHandler()
        tweet_handler = TweetHandler()
        message = message_handler.get_message()
        tweet_handler.post_tweet(message)
