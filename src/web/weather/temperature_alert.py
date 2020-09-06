import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
from src.web.tweet.tweet_handler import TweetHandler
from src.web.util.config_handler import ConfigHandler
from src.web.weather.weather_handler import AmedasWeatherHandler, AmedasWetherInfo
from src.web.util.time_util import TimeUtil
import codecs

if __name__ == "__main__":
    threshold_temperature = 30 # アラートを上げる気温のしきい値

    # 過去にアラートをあげた日付を、気温を取得
    config_handler = ConfigHandler()
    file_path = config_handler.get_temperature_exceed_state_path()
    f = codecs.open(file_path, "r", "utf-8")
    content = f.read().strip()
    f.close()
    last_alert_date = content.split(",")[0]
    last_alert_temp = float(content.split(",")[1])
    current_time = TimeUtil.get_current_time_str().split()[0]

    # 現在の気温を取得
    weather_handler = AmedasWeatherHandler()
    info = weather_handler.fetch_realtime_weather_info()

    # アラートを出すか判定
    alert_flag = False
    if current_time == last_alert_date:
        # 同日に既にアラートがあがっている場合、最高気温を更新していたらアラートを出す
        if info.temp > last_alert_temp + 1:
            alert_flag = True
    else:
        # 同日にアラートがあがっていない場合、気温がしきい値を超えていたらアラートを出す
        if info.temp > threshold_temperature:
            alert_flag = True

    if alert_flag:
        tweet_handler = TweetHandler()
        message_str = "あつーい！いま" + str(info.temp) + "℃もあるわ～💦\n水分補給を忘れずにね❣\n"
        message_str += "#ディズニーランド #東京ディズニーシー #TDL #TDS\n"
        tweet_handler.post_tweet(message_str)
        # アラートを上げた日次を更新
        f = codecs.open(file_path, "w", "utf-8")
        f.write(current_time+","+str(info.temp))
        f.close()


