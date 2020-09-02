import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.web.tweet.tweet_handler import TweetHandler
from src.web.util.config_handler import ConfigHandler
from src.web.util.time_util import TimeUtil
from src.web.word_cloud.word_cloud_maker import WordCloudMaker, WordClass


class PostTDRNowWordCloud:
    def __init__(self):
        self.hash_tag = "#TDR_now"
        config_handler = ConfigHandler()
        self.image_path = config_handler.get_word_cloud_image_path()
        self.tdr_now_tweet_num_per_day = 100 # 1日あたりの「TDR_now」のツイート数の上限値。とりあえず決め打ちで設定

    def post_tdr_now_word_cloud(self):
        ''' #TDR_now のツイートを取得し、ワードクラウドを作成・ツイートする
        '''
        # TDR_nowのツイートを取得する
        current_time = TimeUtil.get_current_time_str().split(" ")[0] # 08月23日
        tweet_handler = TweetHandler()
        tweet_list = tweet_handler.fetch_tweets(self.hash_tag,  self.tdr_now_tweet_num_per_day)

        # ワードクラウド作成対象の文章を作成する
        target_str = ""
        for tweet in tweet_list:
            # 本日の日付でなければワードクラウドに入れない
            # if tweet.created_at.split(" ")[0] != current_time:
            #     continue
            # リツイートやいいねがついているツイートは、多めにカウントする
            for i in range(1 + int(tweet.favorite_count) + int(tweet.retweet_count)):
                # URLは文章に入れない。「TDR」「now」も入れない。
                target_str += tweet.text.split("https")[0].replace("TDR","").replace("now","").replace("tdr","") + " "

        # ターゲットの文章を形態素解析する
        word_cloud_maker = WordCloudMaker()
        word_class_list = word_cloud_maker.decompose_words(target_str)
        target_word_list = []
        for word_class in word_class_list:
            # 品詞が名詞以外であればスキップ
            if "名詞" not in word_class.word_class:
                continue
            # 単語長さが1以下であればスキップ
            if len(word_class.target_word) <= 1:
                continue
            target_word_list.append(word_class.target_word)

        # ワードクラウドを作成
        word_cloud_maker.make_word_cloud_image(target_word_list)

        # 作成したワードクラウドをツイート
        tweet_str = "今日はパークでこんなことがあったみたい！うふふ💕\n"
        tweet_str += "#ディズニーランド #東京ディズニーシー #TDL #TDS\n"
        tweet_handler.post_tweet_with_img(tweet_str, self.image_path)

if __name__ == "__main__":
    handler = PostTDRNowWordCloud()
    handler.post_tdr_now_word_cloud()
