import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.util.config_handler import ConfigHandler
import json


class ApiKeyHandler:
    def __init__(self):
        config_handler = ConfigHandler()
        self.api_key_path =config_handler.get_api_key_path()

    def get_twitter_api_keys(self):
        json_open = open(self.api_key_path, 'r')
        json_load = json.load(json_open)
        api_key = json_load["twitter"]["api_key"]
        api_secret_key = json_load["twitter"]["api_secret_key"]
        access_token = json_load["twitter"]["access_token"]
        secret_access_token = json_load["twitter"]["secret_access_token"]
        return api_key, api_secret_key, access_token, secret_access_token

    def get_open_weather_api_id(self):
        json_open = open(self.api_key_path, 'r')
        json_load = json.load(json_open)
        app_id = json_load["open_weather_map"]["app_id"]
        return app_id


if __name__ == "__main__":
    api_key_handler = ApiKeyHandler()
    print(api_key_handler.get_twitter_api_keys())