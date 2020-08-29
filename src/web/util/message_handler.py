import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.util.config_handler import ConfigHandler
from src.tweet.tweet_handler import TweetHandler
import json
import random


class MessageHandler:
    def __init__(self):
        config_handler = ConfigHandler()
        message_path = config_handler.get_message_path()
        json_open = open(message_path, 'r', encoding="utf-8")
        json_load = json.load(json_open)
        self.message = json_load["message"]

    def get_message(self):
        '''メッセージの中からランダムに一件を取得する。
        '''
        index = random.randrange(len(self.message))
        return self.message[index]

    def get_message_list(self):
        '''メッセージ一覧を取得する。
        '''
        return self.message

if __name__ == "__main__":
    message_handler = MessageHandler()
    print(message_handler.get_message_list())
    message_str = message_handler.get_message()
    print(message_str)

    tweet_handler = TweetHandler()
    tweet_handler.post_tweet(message_str)