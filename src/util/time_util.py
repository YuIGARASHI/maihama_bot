import sys
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/")
sys.path.append("/home/users/0/her.jp-everyday-micmin/web/maihama_bot/vendor")
import datetime

class TimeUtil:
    def __init__(self):
        pass

    @staticmethod
    def unixtime_to_datetime(unixtime):
        return datetime.datetime.fromtimestamp(int(unixtime))

    @staticmethod
    def unixtime_to_datestr(unixtime):
        datetime_obj = TimeUtil.unixtime_to_datetime(unixtime)
        return datetime_obj.strftime('%m月%d日 %H:%M')

    @staticmethod
    def get_current_time_str():
        return datetime.datetime.now().strftime('%m月%d日 %H:%M') # 例：08月23日 20:00


if __name__ == "__main__":
    print(TimeUtil.unixtime_to_datetime(1597280106))
    print(TimeUtil.unixtime_to_datetime("1597280106")) # 文字列でもOK
    print(TimeUtil.unixtime_to_datestr("1597280106"))  # => 08月13日 09:55
    print(TimeUtil.get_current_time_str())