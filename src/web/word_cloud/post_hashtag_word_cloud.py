import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.web.util.api_key_handler import ApiKeyHandler
import tweepy
from src.web.tweet.tweet_handler import TweetHandler

# おためし。ワードクラウド用
from PIL import Image
import numpy as np
import wordcloud, codecs
import MeCab

if __name__ == "__main__":
    api_key_handler = ApiKeyHandler()
    api_key, api_secret_key, access_token, secret_access_token = api_key_handler.get_twitter_api_keys()
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, secret_access_token)
    api = tweepy.API(auth)

    q_word = "#TDR_now -filter:retweets"
    text = ""
    for tweet in tweepy.Cursor(api.search, q=q_word).items(100):
        # お気に入りやリツイートされたツイートは多めにカウント
        for i in range(1 + int(tweet.favorite_count/2) + int(tweet.retweet_count/2)):
            text += tweet.text.split("https")[0] + " "

    # おためしで、ワードクラウドをつくる
    msk = np.array(Image.open('mickey-circle.jpg'))

    m = MeCab.Tagger("")
    text = text.replace('\r', '')
    parsed = m.parse(text)

    splitted = []
    skip_word_list = ["TDR", "tdr", "now", "https", "co", "です", "まし", "けど", "まで", "から", "こと", "ディズニー", "天気", "TDS"]
    skip_word_list = []
    for line in parsed.splitlines():
        elems = line.split("\t")
        if len(elems)  <= 4:
            continue
        word = elems[0].strip()
        type = elems[4]
        if word in skip_word_list:
            continue
        if "名詞" not in type:
            continue
        if len(word) <= 3: # 長さが3以下の文字列はスキップ
            continue
        splitted.append(word)
    wordc = wordcloud.WordCloud(font_path='HGRGM.TTC',
                                background_color='white',
                                # mask=msk,
                                width=1280,
                                collocations=False,
                                height=960).generate(" ".join(splitted))

    wordc.to_file('tdr_now.png')

    # メッセージを構築
    message = "昨日はパークでこんなことがあったみたい！うふふ💕\n"

    # ツイッターに投稿する
    tweet_handler = TweetHandler()
    tweet_handler.post_tweet_with_img(message, 'C:/Users/Yu IGARASHI/PycharmProjects/maihama_bot/src/web/word_cloud/tdr_now.png')
