import os

class ConfigHandler:
    '''ローカルと本番環境のパスの違いを吸収する。
    とりあえずローカルのパスをべた書きしている...
    '''
    def __init__(self):
        self.local_root = "C:/Users/Yu IGARASHI/PycharmProjects/maihama_bot/"
        self.lolipop_root = "/home/users/0/her.jp-everyday-micmin/web/maihama_bot/"

    def get_api_key_path(self):
        if self.is_local():
            return self.local_root + "config/api_key.json"
        else:
            return self.lolipop_root + "config/api_key.json"

    def get_keiyo_line_status_path(self):
        if self.is_local():
            return self.local_root + "tmp/keiyo_line_status.txt"
        else:
            return self.lolipop_root + "tmp/keiyo_line_status.txt"

    def get_news_release_status_path(self):
        if self.is_local():
            return self.local_root + "tmp/news_release_status.txt"
        else:
            return self.lolipop_root+ "tmp/news_release_status.txt"

    def is_local(self):
        if os.path.exists(self.local_root):
            return True
        else:
            return False


if __name__ == "__main__":
    config_handler = ConfigHandler()
    print(config_handler.get_api_key_path())