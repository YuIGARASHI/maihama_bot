import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
import urllib.request as req
from bs4 import BeautifulSoup
from src.tweet.tweet_handler import TweetHandler

class ShoppingHandler:
    def __init__(self):
        self.url = "https://www.disney.co.jp/shopping/special/minnie.html"

    def fetch_minnie_shopping_info(self):
        res = req.urlopen(self.url)
        soup = BeautifulSoup(res, "html.parser")
        cmp_shop_sub = soup.find(class_="cmpShopSub")
        name = cmp_shop_sub.find(class_="data").find("p").text
        goods_link = cmp_shop_sub.find("a").get("href")
        return name, goods_link, self.url

if __name__ == "__main__":
    shopping_handler = ShoppingHandler()
    name, link, url = shopping_handler.fetch_minnie_shopping_info()

    # 以下、おためしでツイート
    tweet_handler = TweetHandler()
    tweet_str = "ミニーのグッズ情報が更新されたよ～💕\n\n"
    tweet_str += "【🎀" + name + "】" + "\n"
    tweet_str += "商品ページ👉 " + link  + "\n\n"
    tweet_str += url
    tweet_handler.post_tweet(tweet_str)