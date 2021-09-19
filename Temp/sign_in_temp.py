import datetime
import time

import requests

# 参数列表
username = [""]  # 用户名
password = [""]  # 密码
answers = ["['0','1','36.5']"]  # 选项及体温
longitude = ["108.90281"]  # 经度
latitude = ["34.15293"]  # 纬度
country = ["中国"]  # 国家
province = ["陕西省"]  # 省份
city = ["西安市"]  # 市
district = ["长安区"]  # 区
township = ["韦曲街道"]  # 街道
street = ["西长安街"]  # 地址
areaCode = ["610116"]  # 行政区划代码


def SignIn(user_flag, area_flag):
    login_url = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username?username=" \
                + username[user_flag] + "&password=" + password[user_flag]
    sign_in_url = "https://student.wozaixiaoyuan.com/health/save.json?answers=" \
                  + answers[area_flag] + "&latitude=" + latitude[area_flag] + "&longitude=" + longitude[area_flag] \
                  + "&country=" + country[area_flag] + "&city=" + city[area_flag] + "&district=" + district[area_flag] \
                  + "&province=" + province[area_flag] + "&township=" + township[area_flag] + "&street=" \
                  + street[area_flag] + "&areacode=" + areaCode[area_flag]
    user_resp = requests.get(login_url)
    user_resp.cookies.set("JWSESSION", value=user_resp.cookies.get('JWSESSION'), domain="student.wozaixiaoyuan.com")
    sign_in_resp = requests.get(sign_in_url, cookies=user_resp.cookies)
    return sign_in_resp.text


if __name__ == "__main__":
    i = 0
    while i < 3:
        time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8.0)  # 获取时间
        if time_now.hour >= 18:
            # 时间未到，等待至下一小时的第一分钟，(^ v ^)
            time.sleep((61 - time_now.minute) * 60)
            continue
        val = SignIn(0, 0)  # 请求
        print(val)
        if val == "{\"code\":0}":
            requests.get("https://sctapi.ftqq.com/SCT64859T79zOCMblEp1OhxlhneFlDWZv.send?title=" \
                         + "签到通知&desp=" + str(time_now.strftime("%Y-%m-%d %H:%M:%S")) + "签到成功！")  # 提示
            break
        else:
            requests.get("https://sctapi.ftqq.com/SCT64859T79zOCMblEp1OhxlhneFlDWZv.send?title=" \
                         + "错误通知&desp=" + str(time_now.strftime("%Y-%m-%d %H:%M:%S")) + "出现错误，错误代码" + \
                         str(val) + "，尝试中，第" + str(i + 1) + "次尝试！")  # 提示
            time.sleep(60)  # 停止60s后重试
            i += 1
