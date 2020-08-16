import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
import requests
import codecs
from bs4 import BeautifulSoup
from src.util.config_handler import ConfigHandler
from src.tweet.tweet_handler import TweetHandler
import datetime

class NewsReleaseHandler:
    def __init__(self):
        self.url = "http://www.olc.co.jp/ja/news.html"

    def fetch_news_release(self):
        '''「東京ディズニーリゾート」タブのニュースリリースの最新1件を取得する
        http://www.olc.co.jp/ja/news.html
        '''
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, "html.parser")
        tab_items = soup.find_all(class_="tabItems")
        target_a_tag = tab_items[1].find_all("a")[0]
        news_release_text = target_a_tag.text.strip()
        news_release_link = target_a_tag.get("href")
        return news_release_text, news_release_link

    def check_and_update_state(self, new_status):
        '''ニュースリリースが更新されている場合にはTrue, されていなければFalseを返す。
        '''
        config_handler = ConfigHandler()
        file_path = config_handler.get_news_release_status_path()
        f = codecs.open(file_path, "r", "utf-8")
        content = f.read()
        f.close()
        if content in new_status:
            return False
        else:
            # 情報を更新する
            f_new = codecs.open(file_path, "w", "utf-8")
            f_new.write(new_status)
            f_new.close()
            return True

    def make_tweet_str(self, news_release_text, news_release_link):
        tweet_str = "【TDRニュースリリース更新情報】\n"
        tweet_str += ("（" + datetime.datetime.now().strftime('%m月%d日 %H:%M') + "）\n\n")
        tweet_str += news_release_text + "\n"
        tweet_str += self.url + "\n"
        return tweet_str
