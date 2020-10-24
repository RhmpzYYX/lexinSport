# -*- coding: UTF-8 -*-
# by rhmpz
# @Time : 2020/10/24 19:50
# @Author : RhmpzYYX
# @File : randomstep.py
import requests
import json
import hashlib
import time
import datetime
import random

'''
项目意义：
如果你想在支付宝蚂蚁森林收集很多能量种树，为环境绿化出一份力量，
又或者是想每天称霸微信运动排行榜装逼，却不想出门走路，那么该 Python 脚本可以帮你实现。
使用方法：
手机安装第三方软件乐心健康，注册账号登录，将运动数据同步到微信和支付宝。用 Python 脚本远程修改乐心健康当前登录账号的步数即可
运行 Python 脚本，修改乐心健康步数。
'''
class LexinSport:
    def __init__(self, username, password, step):
        self.username = username
        self.password = password
        self.step = step

    # 登录
    def login(self):
        url = 'https://sports.lifesense.com/sessions_service/login?systemType=2&version=4.6.7'
        data = {'loginName': self.username, 'password': hashlib.md5(self.password.encode('utf8')).hexdigest(),
                'clientId': '49a41c9727ee49dda3b190dc907850cc', 'roleType': 0, 'appType': 6}
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; LIO-AN00 Build/LIO-AN00)'
        }
        response_result = requests.post(url, data=json.dumps(data), headers=headers)
        status_code = response_result.status_code
        response_text = response_result.text
        # print('登录状态码：%s' % status_code)
        # print('登录返回数据：%s' % response_text)
        if status_code == 200:
            response_text = json.loads(response_text)
            user_id = response_text['data']['userId']
            access_token = response_text['data']['accessToken']
            return user_id, access_token
        else:
            return '登录失败'

    # 修改步数
    def change_step(self):
        # 登录结果
        login_result = self.login()
        if login_result == '登录失败':
            return '登录失败'
        else:
            url = 'https://sports.lifesense.com/sport_service/sport/sport/uploadMobileStepV2?systemType=2&version=4.6.7'
            data = {'list': [{'DataSource': 2, 'active': 1, 'calories': int(self.step/4), 'dataSource': 2,
                              'deviceId': 'M_NULL', 'distance': int(self.step/3), 'exerciseTime': 0, 'isUpload': 0,
                              'measurementTime': time.strftime('%Y-%m-%d %H:%M:%S'), 'priority': 0, 'step': self.step,
                              'type': 2, 'updated': int(round(time.time() * 1000)), 'userId': login_result[0]}]}
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Cookie': 'accessToken=%s' % login_result[1]
            }
            response_result = requests.post(url, data=json.dumps(data), headers=headers)
            status_code = response_result.status_code
            # response_text = response_result.text
            # print('修改步数状态码：%s' % status_code)
            # print('修改步数返回数据：%s' % response_text)
            if status_code == 200:
                return '修改步数为【%s】成功' % self.step
            else:
                return '修改步数失败'


# 睡眠到第二天执行修改步数的时间
def get_sleep_time():
    # 第二天日期
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    # 第二天7点时间戳
    # tomorrow_run_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) + 25200
    # 第二天中午12:30点时间戳 #12.5h*60min*60s=45000
    tomorrow_run_time = int(time.mktime(time.strptime(str(tomorrow), '%Y-%m-%d'))) + 45000
    # print(tomorrow_run_time)
    # 当前时间戳
    current_time = int(time.time())
    # print(current_time)
    return tomorrow_run_time - current_time


if __name__ == "__main__":
    #random():随机设置每天步数
    stepsrandom=random.randint(20000,40000)
    print(stepsrandom)
    # 最大运行出错次数
    fail_num = 3
    while 1:
        while fail_num > 0:
            try:
                # 修改步数结果
                # result = LexinSport('乐心健康账号', '乐心健康密码', 修改步数).change_step()
                result = LexinSport('13552838690', '19990503005', stepsrandom).change_step()
                '''
程序设定是每天 7 点自动修改步数，在下面脚本对应的位置替换填入乐心健康账号、乐心健康密码、修改步数，然后运行程序。
修改步数推荐设置范围是 30000 至 90000，步数值太大会导致修改不成功。如果想改变第二天自动修改步数的时间，请修改图示位置的 25200，+25200 
代表第二天 0 点后加上的秒数，也就是 7x60x60，即 7 小时，根据自己的需要修改即可。如果每天都要修改步数，那么让程序一直保持运行即可。
注意：运行程序会立刻修改当天的步数，自动修改步数是从程序保持运行的第二天开始。
                '''
                print(result)
                break
            except Exception as e:
                print('运行出错，原因：%s' % e)
                fail_num -= 1
                if fail_num == 0:
                    print('修改步数失败')
        # 重置运行出错次数
        fail_num = 3
        # 获取睡眠时间
        sleep_time = get_sleep_time()
        time.sleep(sleep_time)
