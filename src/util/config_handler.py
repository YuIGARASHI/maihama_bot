import os

class ConfigHandler:
    '''ローカルと本番環境のパスの違いを吸収する。
    とりあえずローカルのパスをべた書きしている...
    '''
    def __init__(self):
        self.local_roots = [
            "C:/Users/Yu IGARASHI/PycharmProjects/maihama_bot/",
            "C:/Users/yukodev/dev/maihama_bot"
        ]
        self.lolipop_root = "/home/users/0/her.jp-everyday-micmin/web/maihama_bot/"

    def get_api_key_path(self):
        base_path = "config/api_key.json"
        return self.select_root_path() + base_path

    def get_keiyo_line_status_path(self):
        base_path = "tmp/keiyo_line_status.txt"
        return self.select_root_path() + base_path

    def get_message_path(self):
        base_path = "static_data/message.json"
        return self.select_root_path() + base_path

    def get_temperature_exceed_state_path(self):
        base_path = "tmp/temperature_exceed_state.txt"
        return self.select_root_path() + base_path

    def get_shopping_state_path(self):
        base_path = "tmp/shopping_goods_state.txt"
        return self.select_root_path() + base_path

    def select_root_path(self):
        for path in self.local_roots:
            if os.path.exists(path):
                return path
        return self.lolipop_root

if __name__ == "__main__":
    config_handler = ConfigHandler()
    print(config_handler.get_api_key_path())