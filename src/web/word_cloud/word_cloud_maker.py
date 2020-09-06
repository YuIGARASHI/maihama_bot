import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
from src.web.util.config_handler import ConfigHandler
import MeCab
import wordcloud
import numpy as np
from PIL import Image


class WordClass:
    def __init__(self, word_str):
        splited = word_str.split("\t")
        self.target_word = ""
        self.word_class = ""
        if len(splited) <=4:
            return
        self.target_word = splited[0]  # 対象の語。例：「サンプル」
        self.word_class = splited[4]   # 品詞。例：「名詞-普通名詞-一般」


class WordCloudMaker:
    def __init__(self):
        config_handler = ConfigHandler()
        self.image_path = config_handler.get_word_cloud_image_path()

    def decompose_words(self, sentence):
        '''文章の形態素解析を実施する。

        Return
        ------
        word_class_list : array-like(WordClass)
            sentenceを形態素解析して出現した語のオブジェクト配列。
        '''
        # 辞書のパスはローカルのものをベタ打ち
        m = MeCab.Tagger("-d \"C:\Program Files\MeCab\dic\ipadic\"")
        text = sentence.replace('\r', '')
        parsed_content = m.parse(text)
        word_class_list = []
        for line in parsed_content.splitlines():
            word_class = WordClass(line)
            word_class_list.append(word_class)
        return word_class_list

    def make_word_cloud_image(self, word_list):
        '''ワードクラウドを生成する。
        '''
        # ミッキーの型にする
        config_handler = ConfigHandler()
        image_path = config_handler.get_mickey_image_path()
        mask = np.array(Image.open(image_path))
        wordc = wordcloud.WordCloud(font_path='HGRGM.TTC',
                                    background_color='white',
                                    width=1280,
                                    colormap="spring",
                                    collocations=False,
                                    mask=mask,
                                    height=960).generate(" ".join(word_list))
        wordc.to_file(self.image_path)

    def make_sample(self, target_str):
        '''サンプルのワードクラウドを作成する。

        ・すべての品詞が対象
        ・すべての長さの語が対象
        ※元の文章の語に何らかのフィルタをかけたい場合などは、
        呼び出し元でフィルタをかけてからmake_word_cloud_image_from_strなどを呼び出すこと。
        '''
        word_class_list = self.decompose_words(target_str)
        word_list = []
        for word_class in word_class_list:
            word_list.append(word_class.target_word)
        self.make_word_cloud_image(word_list)


if __name__=="__main__":
    word_cloud_maker = WordCloudMaker()
    ret_list = word_cloud_maker.decompose_words("これはサンプルの文章です。")
    for word_class in ret_list:
        print(word_class.target_word, word_class.word_class)
    # word_cloud_maker.make_sample("これはサンプルの文章です。")