import datetime
import os
import random

import requests

# 参数列表
username = ["18292162941"]  # [""]   用户名
password = ["q2w3e4"]  # [""]   密码
user = ["FuXuXiang"]  # 企业微信用户名列表
corpId = os.environ['CorpId']  # 企业微信企业代码
corpSecret = os.environ['CorpSecret']  # 企业微信应用secret
answers = ["['0','1','" + str(36 + random.randint(3, 7) / 10.0) + "']"]  # 选项及体温
longitude = ["108.90281"]  # 经度
latitude = ["34.15293"]  # 纬度
country = ["中国"]  # 国家
province = ["陕西省"]  # 省份
city = ["西安市"]  # 市
district = ["长安区"]  # 区
township = ["韦曲街道"]  # 街道
street = ["西长安街"]  # 地址
areaCode = ["610116"]  # 行政区划代码
https://gw.wozaixiaoyuan.com/basicinfo/mobile/my/changePassword?newPassword=q2w3e4&oldPassword=q2w3e4


def ReInf(res, user_flag):
    if res["user_resp"].json()['code'] == 0 & res["sign_in_resp"].json()['code'] == 0:
        requests.post(url=getUrl(), json=ReData("签到通知\n" + getTimeStr() + " 签到成功！", user_flag))
    elif res["user_resp"].json()['code'] == 0:
        requests.post(url=getUrl(), json=ReData("错误通知\n" + getTimeStr() + " 出现错误，错误原因{" + \
                                                "无" + ", " + \
                                                res["sign_in_resp"].json()['message'] + "}，尝试中断", user_flag))
    else:
        requests.post(url=getUrl(), json=ReData("错误通知\n" + getTimeStr() + " 出现错误，错误原因{" + \
                                                res["user_resp"].json()['message'] + ", " + \
                                                res["sign_in_resp"].json()['message'] + "}，尝试中断", user_flag))


def ReData(string, user_flag):
    return {
        "touser": user[user_flag],
        "msgtype": "text",
        "agentid": 1000003,
        "text": {
            "content": str(string)
        }
    }


def getTimeStr():
    time_now = datetime.datetime.utcnow() + datetime.timedelta(hours=8.0)  # 获取时间
    return str(time_now.strftime("%Y-%m-%d %H:%M:%S"))


def SignIn(user_flag, area_flag):
    login_url = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username?username=" \
                + username[user_flag] + "&password=" + password[user_flag]
    sign_in_url = "https://student.wozaixiaoyuan.com/health/save.json?answers=" \
                  + answers[area_flag] + "&latitude=" + latitude[area_flag] + "&longitude=" + longitude[area_flag] \
                  + "&country=" + country[area_flag] + "&city=" + city[area_flag] + "&district=" + district[area_flag] \
                  + "&province=" + province[area_flag] + "&township=" + township[area_flag] + "&street=" \
                  + street[area_flag] + "&areacode=" + areaCode[area_flag]
    change_url = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/my/changePassword?newPassword=" + \
                 password[user_flag] + "&oldPassword=" + password[user_flag]
    user_resp = requests.get(login_url)
    change_resp = requests.get(change_url, cookies=user_resp.cookies)
    user_resp.cookies.set("JWSESSION", value=user_resp.cookies.get('JWSESSION'), domain="student.wozaixiaoyuan.com")
    sign_in_resp = requests.get(sign_in_url, cookies=user_resp.cookies)
    return {"user_resp": user_resp, "sign_in_resp": sign_in_resp, "change_resp": change_resp}

def getUrl():
    return "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + requests.get(
        "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpId + "&corpsecret=" + corpSecret).json()[
        'access_token']


def main():
    res = SignIn(0, 0)  # 请求
    ReInf(res, 0)
    print(getTimeStr() + " 打卡完毕")


if __name__ == "__main__":
    main()
