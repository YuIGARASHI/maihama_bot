import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
from src.tweet.tweet_handler import TweetHandler
from src.util.config_handler import ConfigHandler
from src.weather.weather_handler import AmedasWeatherHandler, AmedasWetherInfo
from src.util.time_util import TimeUtil
import codecs

if __name__ == "__main__":
    threshold_temperature = 30 # アラートを上げる気温のしきい値

    # 過去にアラートをあげた日付を取得
    config_handler = ConfigHandler()
    file_path = config_handler.get_temperature_exceed_state_path()
    f = codecs.open(file_path, "r", "utf-8")
    content = f.read()
    f.close()
    current_time = TimeUtil.get_current_time_str().split()[0]
    # 同日であれば処理を打ち切る
    if current_time == content.strip():
        exit()

    # 気温がしきい値を超えていればアラートを出す
    weather_handler = AmedasWeatherHandler()
    info = weather_handler.fetch_realtime_weather_info()
    if info.temp > threshold_temperature:
        tweet_handler = TweetHandler()
        tweet_handler.post_tweet("あつーい！いま" + str(info.temp) + "℃もあるわ～💦\n水分補給を忘れずにね❣")
        # アラートを上げた日次を更新
        f = codecs.open(file_path, "w", "utf-8")
        f.write(current_time)
        f.close()


