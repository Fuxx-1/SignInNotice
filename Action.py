# -*- coding: gbk -*-import datetimeimport osimport requests# 参数列表corpId = os.environ['CorpId']  # 企业微信企业代码corpSecret = os.environ['CorpSecret']  # 企业微信应用secretdef getAccessToken():    return requests.get(        "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpId + "&corpsecret=" + corpSecret).json()[        'access_token']userlist = requests.get(    url="https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=" + getAccessToken() + "&fetch_child=FETCH_CHILD&department_id=3").json()[    "userlist"]  # 企业微信用户名列表def getTime():    return datetime.datetime.utcnow() + datetime.timedelta(hours=8.0)  # 获取时间def sendMessage(userid, message):    requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + getAccessToken(), json={        "touser": str(userid),        "msgtype": "text",        "agentid": 1000003,        "text": {            "content": str(message)        }    })def main():    for user in userlist:        print(user["userid"])        sendMessage(user["userid"], "打卡提示\n已打卡请忽略 [旺柴]\n<a href=\"https://gw.wozaixiaoyuan.com/h5/mobile/basicinfo/index/\">🔗微信环境下点我去打卡</a>")        if getTime().hour >= 12:            sendMessage(user, "--------今日提示完毕--------")        print("提示完毕")if __name__ == "__main__":    main()