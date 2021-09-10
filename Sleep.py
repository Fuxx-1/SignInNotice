import datetime
import time

if __name__ == "__main__":
    while True:
        time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8.0)  # 获取时间
        if time_now.hour == 7 | time_now.hour == 12 | time_now.hour == 16:
            break
        else:
            # 时间未到，等待至下一小时的第30分钟，(^ v ^)
            time.sleep((90 - time_now.minute) * 60)
            continue
    print("---倒计时完毕---")