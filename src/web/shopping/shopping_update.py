import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.web.shopping.shopping_handler import ShoppingHandler
from src.web.util.config_handler import ConfigHandler
from src.web.tweet.tweet_handler import TweetHandler
import codecs

if __name__ == "__main__":
    # 過去の商品情報を取得
    config_handler = ConfigHandler()
    file_path = config_handler.get_shopping_state_path()
    f = codecs.open(file_path, "r", "utf-8")
    content = f.read()
    f.close()

    # 現在の商品情報を取得
    shopping_handler = ShoppingHandler()
    name, goods_link, url = shopping_handler.fetch_minnie_shopping_info()
    if name == content.strip():
        exit()

    # 商品情報をアップデート
    tweet_handler = TweetHandler()
    tweet_str = "ミニーのグッズ情報が更新されたよ～💕\n\n"
    tweet_str += "【🎀" + name + "】" + "\n"
    tweet_str += "商品ページ👉 " + goods_link  + "\n\n"
    tweet_str += url
    tweet_handler.post_tweet(tweet_str)
    f = codecs.open(file_path, "w", "utf-8")
    f.write(name)
    f.close()