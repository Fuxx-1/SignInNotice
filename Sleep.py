import datetime
import time

if __name__ == "__main__":
    while True:
        time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8.0)  # 获取时间
        if time_now.hour >= 18:
            # 时间未到，等待至下一小时的第一分钟，(^ v ^)
            time.sleep((61 - time_now.minute) * 60)
            continue
        else:
            break
