import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.web.util.api_key_handler import ApiKeyHandler
from src.web.util.time_util import TimeUtil
import json
import requests
import datetime
import urllib.request as req
from bs4 import BeautifulSoup


class WeatherEnum(enumerate):
    Clear = 0  # 晴れ
    Rain = 1   # 雨
    Clouds = 2  # 曇り
    Snow = 3    # 雪
    Thunderstorm = 4 # 雷雨
    Other = 5   # その他


class OWMWeatherInfo:
    ''' OpenWeatherMapの天気情報クラス。
    '''
    def __init__(self, json_info):
        # 天気
        self.weather = OWMWeatherInfo.str_to_weather(json_info["weather"][0]["main"]) # とりあえず0番目だけ取得する
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
        print("天気：" + OWMWeatherInfo.weather_to_str(self.weather))
        print("時刻：" + self.time)
        print("気温：" + self.temp)
        print("降水確率：" + self.pop)
        print("湿度：" + self.humidity)
        print("雲量：" + self.clouds)
        print("風速：" + self.wind_speed)


class AmedasWetherInfo:
    '''アメダスの天気情報を保持するクラス。
    '''
    def __init__(self):
        self.temp = -1 # 気温

    def print_myself(self):
        print("気温：" + str(self.temp))


class OWMWeatherHandler:
    '''OpenWeatherMapから天気情報を取得するクラス。

    One Call API
    https://openweathermap.org/api/one-call-api
    '''
    def __init__(self):
        self.city_str = "Urayasu"
        self.endpoint = "https://api.openweathermap.org/data/2.5/onecall"
        self.maihama_lat = "35.6335425"
        self.maihama_lon = "139.8750675"
        self.lang = "ja"
        api_key_handler = ApiKeyHandler()
        self.app_id = api_key_handler.get_open_weather_api_id()

    def get_target_time_index(self, weather_json):
        '''翌日の12:00に該当するインデクスを取得する。
        '''
        now_date = datetime.datetime.now().strftime('%m月%d日')
        target_index = -1
        for i in range(len(weather_json["hourly"])):
            target_time_str = TimeUtil.unixtime_to_datestr(weather_json["hourly"][i]["dt"])
            # 日付が翌日のものになるまでループ
            if now_date in target_time_str:
                continue
            if "12:00" in target_time_str:
                target_index = i
            if target_index != -1:
                break # このbreakがないと、翌々日の9:00と17:00のインデクスを取得してしまう可能性がある
        return target_index

    def fetch_tomorrow_weather_info(self):
        '''翌日の12:00の天気情報を取得する。
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
        target_index = self.get_target_time_index(weather_json)
        weather_info = OWMWeatherInfo(weather_json["hourly"][target_index])
        return weather_info

class AmedasWeatherHandler:
    '''アメダスから天気情報を取得するクラス。
    '''
    def __init__(self):
        # 「江戸川臨海」のアメダス情報
        self.url = "https://tenki.jp/amedas/3/16/44136.html"

    def fetch_realtime_weather_info(self):
        '''リアルタイムの気象情報をアメダスから取得する。
        '''
        res = req.urlopen(self.url)
        soup = BeautifulSoup(res, "html.parser")
        weather_info = AmedasWetherInfo()
        # 最新時刻の気温取得
        weather_info.temp = float(soup.find(class_="amedas-table-entries").find_all("td")[2].text)
        return weather_info

if __name__ == "__main__":
    # weather_handler = OWMWeatherHandler()
    # weather_info = weather_handler.fetch_tomorrow_weather_info()
    # weather_info.print_myself()

    weather_handler = AmedasWeatherHandler()
    weather_info = weather_handler.fetch_realtime_weather_info()
    weather_info.print_myself()