import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
import urllib.request as req
from bs4 import BeautifulSoup
import datetime
import codecs
from src.util.config_handler import ConfigHandler

class TrainInfoHandler():
    def __init__(self):
        self.url = "https://transit.yahoo.co.jp/traininfo/detail/69/0/"

    def get_keiyo_line_info(self):
        res = req.urlopen(self.url)
        soup = BeautifulSoup(res, "html.parser")
        service_status = soup.find(id="mdServiceStatus")
        status_summary = service_status.dt.text.split("]")[1]  # => 「平常運転」「その他」
        status_detail = service_status.dd.text
        return status_summary, status_detail

    def make_tweet_str(self, status_detail):
        dt_now = datetime.datetime.now().strftime('%m月%d日 %H:%M')  # => 「02月04日 21:04」
        tweet_str = "【京葉線 運行情報】\n"
        tweet_str += status_detail + "\n"
        tweet_str += self.url
        return tweet_str

    def check_and_update_state(self, status_detail):
        '''
        京葉線の運行情報が更新されている場合true, されていない場合falseを返す
        '''
        config_handler = ConfigHandler()
        file_path = config_handler.get_keiyo_line_status_path()
        f = codecs.open(file_path, "r", "utf-8")
        content = f.read()
        f.close()
        if content in status_detail:
            return False
        else:
            # 情報を更新する
            f_new = codecs.open(file_path, "w", "utf-8")
            f_new.write(status_detail.split("（")[0])
            f_new.close()
            return True

if __name__ == "__main__":
    train_info_handler = TrainInfoHandler()
    status_summary, status_detail = train_info_handler.get_keiyo_line_info()
    print(status_summary, status_detail)
    tweet_str = train_info_handler.make_tweet_str(status_detail)
    print(tweet_str)
    print(train_info_handler.check_and_update_state(status_detail))