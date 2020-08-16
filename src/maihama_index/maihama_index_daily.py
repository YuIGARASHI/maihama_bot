import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.maihama_index.weather_handler import WeatherHandler, WeatherEnum, WeatherInfo
from src.tweet.tweet_handler import TweetHandler
import datetime

class MaihamaIndex:
    def __init__(self):
        self.total_score = 0  # 舞浜指数
        self.rain_score = 0  # 雨
        self.storm_score = 0  # 暴風雨
        self.uv_score = 0  # 紫外線
        self.discomfort_score = 0 # 不快度指数
        self.wind_score = 0  # 風
        self.coldness_score = 0  # 寒さ

    def print_myself(self):
        print("総合スコア：" + str(self.total_score))
        print("雨スコア：" + str(self.rain_score))
        print("暴風雨スコア：" + str(self.storm_score))
        print("紫外線スコア：" + str(self.uv_score))
        print("不快度指数スコア：" + str(self.discomfort_score))
        print("風スコア：" + str(self.wind_score))
        print("寒さスコア：" + str(self.coldness_score))


class MaihamaIndexMaker:
    @staticmethod
    def calc_index(weather_info):
        '''舞浜指数を計算する。
        '''
        maihama_index = MaihamaIndex()

        # 雨スコア
        if weather_info.weather == WeatherEnum.Rain:
            maihama_index.rain_score += 1
        # 降水確率が高い場合はスコアを追加する
        if int(weather_info.pop) > 60:
            maihama_index.rain_score += 1

        # 暴風雨スコア。暴風雨は危険なので巨大なスコアを盛る
        if weather_info.weather == WeatherEnum.Thunderstorm:
            maihama_index.storm_score += 100

        # 紫外線スコア。天気が晴れ & 雲量が少ない場合は紫外線スコアを加算
        if int(weather_info.temp) > 18: # 冬の快晴日を除外するため、気温が低い場合はスキップ
            if weather_info.weather == WeatherEnum.Clear and int(weather_info.clouds) < 30:
                maihama_index.uv_score += 1
                # 夏日であればスコアを加算
                if int(weather_info.temp) > 25:
                    maihama_index.uv_score += 1

        # 不快度指数
        # https://ja.wikipedia.org/wiki/不快度指数
        discomfort_index = 0.81 * int(weather_info.temp) + 0.01 * int(weather_info.humidity) * (0.99 * int(weather_info.temp) - 14.3) + 46.3
        if discomfort_index >= 78:
            maihama_index.discomfort_score += 1
            if discomfort_index >= 85:
                maihama_index.discomfort_score += 1

        # 風スコア。このへんは感覚でやってるので、試行錯誤の余地はけっこうありそう。
        if float(weather_info.wind_speed) > 8:
            maihama_index.wind_score += 1
            if int(weather_info.wind_speed) > 15:
                maihama_index.wind_score += 1

        # 寒さスコア
        if float(weather_info.temp) <= 0:
            maihama_index.coldness_score += 1

        # 合計スコア
        maihama_index.total_score = MaihamaIndexMaker.__calc_total_score(maihama_index)
        return maihama_index

    @staticmethod
    def __calc_total_score(maihama_index):
        return maihama_index.rain_score + maihama_index.storm_score + maihama_index.uv_score + \
            maihama_index.discomfort_score + maihama_index.wind_score + maihama_index.coldness_score

    @staticmethod
    def make_message(maihama_index):
        '''ユーザへの一言メッセージを作成する。
        '''
        # ここはできるだけいろんなバリエーションがあったほうがよい
        # とりあえず仮置き
        if maihama_index.wind_score > 0:
            return "風が強いかも。\n帽子が飛ばされないように気を付けてね！\n"
        if maihama_index.uv_score:
            return "紫外線に注意！\nUVケアを忘れずに～\n"
        if maihama_index.rain_score > 0:
            return "雨にご用心。\nカサを忘れずに楽しんでね♪\n"
        if maihama_index.discomfort_score > 0:
            return "とっても暑い！\nこまめに水分をとって楽しんでね♪\n"
        return "素敵な一日になりそう！\n"

    @staticmethod
    def make_tweet_str(maihama_index, message_str, weather_info):
        '''ツイートする文章を構築する。
        '''
        tweet_str = "【明日の舞浜のお天気☀☁☂☃】\n"
        tweet_str += ("（" + weather_info.time + "）\n\n")

        star = ""
        for i in range(5):
            if i < (5 - maihama_index.total_score/2):
                star += "★"
            else:
                star += "☆"
        tweet_str += (star + "\n")

        # 気象情報
        tweet_str += "天気：" + WeatherInfo.weather_to_str(weather_info.weather) + "\n"
        tweet_str += "降水確率：" + weather_info.pop + "%\n"
        tweet_str += "気温：" + weather_info.temp + "℃\n"
        tweet_str += "湿度：" + weather_info.humidity + "%\n"
        tweet_str += "雲量：" + weather_info.clouds + "%\n"
        tweet_str += "風速：" + weather_info.wind_speed + "m/s\n\n"

        # メッセージ
        tweet_str +=  message_str

        return tweet_str

if __name__ == "__main__":
    weather_handler = WeatherHandler()
    tweet_handler = TweetHandler()
    nine_weather_info, fifteen_weather_info = weather_handler.fetch_tomorrow_weather_info()

    # 9:00
    nine_maihama_index = MaihamaIndexMaker.calc_index(nine_weather_info)
    nine_message = MaihamaIndexMaker.make_message(nine_maihama_index)
    nine_tweet_str = MaihamaIndexMaker.make_tweet_str(nine_maihama_index, nine_message, nine_weather_info)
    tweet_handler.post_tweet(nine_tweet_str)

    # 17:00
    fifteen_maihama_index = MaihamaIndexMaker.calc_index(fifteen_weather_info)
    fifteen_message = MaihamaIndexMaker.make_message(fifteen_maihama_index)
    fifteen_tweet_str = MaihamaIndexMaker.make_tweet_str(fifteen_maihama_index, fifteen_message, fifteen_weather_info)
    tweet_handler.post_tweet(fifteen_tweet_str)

