# -*- coding: utf-8 -*-
"""
cron: 1 6,22 * * *
new Env('名创优品');

微信小程序捉包 https://activity.miniso.com/域名请求头里的content-skey和content-uid

青龙变量 export mcyp_token="uid=xxx&skey=xxxx" 多账号@隔开
"""
import requests
import logging
import time
import os
from notify import send

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

cookies = []
try:
    if "mcyp_token" in os.environ:
        cookies = os.environ["mcyp_token"].split("@")
        if len(cookies) > 0:
            logger.info(f"共找到{len(cookies)}个账号 已获取并使用Env环境Cookie")
            logger.info("声明：本脚本为学习python 请勿用于非法用途")
    else:
        logger.info("【提示】变量格式: skey=xxxx&uid=xxxx\n环境变量添加: mcyp_token")
        exit(3)
except Exception as e:
    logger.error(f"发生错误：{e}")
    exit(3)


# -------------------------分割线------------------------
class miniso:
    @staticmethod
    def setHeaders(skey, uid):
        headers = {
            'Host': 'activity.miniso.com',
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; OPPO R9s Build/NZH54D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5197 MMWEBSDK/20230303 MMWEBID/1571 MicroMessenger/8.0.34.2340(0x2800225F) WeChat/arm64 Weixin NetType/ctlte Language/zh_CN ABI/arm64 MiniProgramEnv/android',
            'content-skey': f'{skey}',
            'content-uid': f'{uid}'
        }
        return headers

    @staticmethod
    def tasklist(headers):
        try:
            url = f'https://activity.miniso.com/fame/task'
            data = {"phone": "null", "avatar": "null"}
            response = requests.post(url=url, headers=headers, json=data)
            result = response.json()
            for task in result['data']['tasks']:
                taskName = task['taskName']
                if '邀请' in taskName or '生日' in taskName or '下单' in taskName:
                    continue  # 跳过包含特定字符串的任务
                if task['taskStatus'] == 0:
                    taskId = task['taskId']
                    res = f"任务: {taskName} -- 未完成"
                    logger.info(res)
                    log_list.append(res)
                    for _ in range(3):
                        miniso.uploadHeartBeatPacket(headers, taskId)
                        time.sleep(5)  # 休眠5秒
                else:
                    res = f"任务: {taskName} -- 已完成"
                    logger.info(res)
                    log_list.append(res)
        except Exception as e:
            print(e)

    @staticmethod
    def uploadHeartBeatPacket(headers, taskId):
        try:
            url = f'https://activity.miniso.com/fame/task/uploadHeartBeatPacket?taskId={taskId}'
            response = requests.get(url=url, headers=headers)
            result = response.json()
            if result['code'] == 200:
                miniso.bpstatus(headers, taskId)
            else:
                res = f"领取任务: {result['message']}"
                logger.info(res)
                log_list.append(res)
        except Exception as e:
            print(e)

    @staticmethod
    def bpstatus(headers, taskId):
        try:
            url = f'https://activity.miniso.com/fame/task/bp/status'
            data = {"taskId": taskId, "avatar": "null", "phone": "null"}
            response = requests.post(url=url, headers=headers, json=data)
            result = response.json()
            if result['code'] == 200:
                res = f"上报: {result['message']}"
                logger.info(res)
                log_list.append(res)
                miniso.obtain(headers, taskId)
            else:
                res = f"上报: {result['description']}"
                logger.info(res)
                log_list.append(res)
        except Exception as e:
            print(e)

    @staticmethod
    def obtain(headers, taskId):
        try:
            url = f'https://activity.miniso.com/fame/task/obtain'
            data = {"taskId": taskId, "avatar": "null", "phone": "null"}
            response = requests.post(url=url, headers=headers, json=data)
            result = response.json()
            res = f"领取: {result['message']}"
            logger.info(res)
            log_list.append(res)
        except Exception as e:
            print(e)

    @staticmethod
    def openBox(headers, uid):
        try:
            url = f'https://activity.miniso.com/fame/openBox'
            data = {"memberAvatar": "null", "memberCode": uid, "phone": "null", "shareMemberCode": "null"}
            response = requests.post(url=url, headers=headers, json=data)
            result = response.json()
            if result['code'] == 200:
                if result['data']['prizeName'] == '名气值':
                    res = f"开箱: 获得{result['data']['value']}名气值"
                    logger.info(res)
                    log_list.append(res)
                    time.sleep(3)  # 休眠3秒
                    miniso.openBox(headers, uid)
                else:
                    res = f"开箱: 获得{result['data']['prizeName']}"
                    logger.info(res)
                    log_list.append(res)
                    time.sleep(3)  # 休眠3秒
                    miniso.openBox(headers, uid)
                    log_list.append(res)
            else:
                res = f"开箱: 获得{result['message']}"
                logger.info(res)
                log_list.append(res)
        except Exception as e:
            print(e)

    @staticmethod
    def signin(headers):
        try:
            url = f'https://activity.miniso.com/fame/getOpenBoxNumber'
            response = requests.get(url=url, headers=headers)
            result = response.json()
            if result['code'] == 200:
                return response.json()
                res = f"签到: 获得{result['data']['openBoxNumber']}次开箱次数"
                logger.info(res)
                log_list.append(res)
            else:
                return response.json()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    log_list = []  # 存储日志信息的全局变量

    for i in range(len(cookies)):
        logger.info(f"\n开始第{i + 1}个账号")
        uid = cookies[i].split('uid=')[1].split('&')[0]
        skey = cookies[i].split('skey=')[1]

        logger.info("--------------日常任务--------------")
        headers = miniso.setHeaders(skey, uid)
        result = miniso.signin(headers)

        if result['code'] == 200:
            miniso.tasklist(headers)
            logger.info("\n--------------开箱任务--------------")
            miniso.openBox(headers, uid)
        else:
            logger.info(f"当前状态: {result['description']}")
            log_list.append(result['description'])

    logger.info("\n============== 推送 ==============")
    send("名创优品", '\n'.join(log_list))
