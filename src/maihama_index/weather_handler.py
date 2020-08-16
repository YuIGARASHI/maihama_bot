'''
OpenWeatherMapから天気情報を取得する。
One Call API
    https://openweathermap.org/api/one-call-api
'''

import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.util.api_key_handler import ApiKeyHandler
from src.util.time_util import TimeUtil
import json
import requests
import datetime


class WeatherEnum(enumerate):
    Clear = 0  # 晴れ
    Rain = 1   # 雨
    Clouds = 2  # 曇り
    Snow = 3    # 雪
    Thunderstorm = 4 # 雷雨
    Other = 5   # その他


class WeatherInfo:
    def __init__(self, json_info):
        # 天気
        self.weather = WeatherInfo.str_to_weather(json_info["weather"][0]["main"]) # とりあえず0番目だけ取得する
        # time
        self.time = TimeUtil.unixtime_to_datestr(json_info["dt"])
        # 摂氏[℃]
        self.temp = str(int(json_info["temp"] - 273.15))
        # 降水確率[%]。Probability of precipitation の略らしい。
        self.pop = str(int(json_info["pop"] * 100))
        # 湿度[%]
        self.humidity = str(json_info["humidity"])
        # 雲量[%]
        self.clouds = str(json_info["clouds"])
        # 風速
        self.wind_speed = str(json_info["wind_speed"])

    @staticmethod
    def str_to_weather(target_str):
        weather_mapping = {
            "Clear": WeatherEnum.Clear,
            "Rain": WeatherEnum.Rain,
            "Clouds": WeatherEnum.Clouds,
            "Snow": WeatherEnum.Snow,
            "Thunderstorm": WeatherEnum.Thunderstorm
        }
        if target_str in weather_mapping:
            return weather_mapping[target_str]
        else:
            return WeatherEnum.Other

    @staticmethod
    def weather_to_str(weather_enum):
        str_mapping = {
            WeatherEnum.Clear: "晴れ ☀",
            WeatherEnum.Rain: "雨 ☂",
            WeatherEnum.Clouds: "曇り ☁",
            WeatherEnum.Snow: "雪 ⛄",
            WeatherEnum.Thunderstorm: "雷雨 ⚡"
        }
        if str_mapping.get(weather_enum):
            return str_mapping[weather_enum]
        else:
            return "その他"

    def print_myself(self):
        print("天気：" + WeatherInfo.weather_to_str(self.weather))
        print("時刻：" + self.time)
        print("気温：" + self.temp)
        print("降水確率：" + self.pop)
        print("湿度：" + self.humidity)
        print("雲量：" + self.clouds)
        print("風速：" + self.wind_speed)


class WeatherHandler:
    def __init__(self):
        self.city_str = "Urayasu"
        self.endpoint = "https://api.openweathermap.org/data/2.5/onecall"
        self.maihama_lat = "35.6335425"
        self.maihama_lon = "139.8750675"
        self.lang = "ja"
        api_key_handler = ApiKeyHandler()
        self.app_id = api_key_handler.get_open_weather_api_id()

    def get_target_time_index(self, weather_json):
        '''翌日の9:00, 17:00に該当するインデクスを取得する。
        '''
        now_date = datetime.datetime.now().strftime('%m月%d日')
        nine_index = -1
        fifteen_index = -1
        for i in range(len(weather_json["hourly"])):
            target_time_str = TimeUtil.unixtime_to_datestr(weather_json["hourly"][i]["dt"])
            # 日付が翌日のものになるまでループ
            if now_date in target_time_str:
                continue
            if "09:00" in target_time_str:
                nine_index = i
            if "17:00" in target_time_str:
                fifteen_index = i
            if nine_index != -1 and fifteen_index != -1:
                break # このbreakがないと、翌々日の9:00と17:00のインデクスを取得してしまう可能性がある
        return nine_index, fifteen_index

    def fetch_tomorrow_weather_info(self):
        '''翌日の朝・夕の情報を取得する。
        '''
        params = {
            "lat": self.maihama_lat,
            "lon": self.maihama_lon,
            "exclude": "current,minutely",
            "appid": self.app_id,
            "lang": self.lang
        }
        response = requests.get(url=self.endpoint, params=params)
        weather_json =  json.loads(response.text)
        nine_index, fifteen_index = self.get_target_time_index(weather_json)
        nine_weather_info = WeatherInfo(weather_json["hourly"][nine_index])
        fifteen_weather_info = WeatherInfo(weather_json["hourly"][fifteen_index])
        return nine_weather_info, fifteen_weather_info


if __name__ == "__main__":
    weather_handler = WeatherHandler()
    nine_weather_info, fifteen_weather_info = weather_handler.fetch_tomorrow_weather_info()
    nine_weather_info.print_myself()
    print("------------------------------------")
    fifteen_weather_info.print_myself()