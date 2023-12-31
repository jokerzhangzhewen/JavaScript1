# -*- coding: utf-8 -*-
"""
cron: 1 9,12,18 * * *
new Env('微信阅读');
地址: http://dst1ya655g.qqaas.fun/app/main?openId=oiDdr50cvXog64PlMEvSfy3V31Hs#/
微信捉包 http://xxxxxx/read/get 域名请求头里的 cookie

注意: 每天第一轮跑之前先手动看大概10篇，遇到2-3次检测文章后再用脚本 
青龙变量 export wxread="authtoken=eyJ0eXAiOiJKV1QiLCJhbxxxxx; snapshot=0" 多账号@隔开
"""
import requests
import logging
import time
import os, re
import json
import random
from notify import send

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    from base64 import b64encode
except:
    logger.info(
        "\n未检测到pycryptodome\n需要Python依赖里安装pycryptodome\n安装失败先linux依赖里安装gcc、python3-dev、libc-dev\n如果还是失败,重启容器,或者重启docker就能解决")
    exit(0)

cookies = []
try:
    if "wxread" in os.environ:
        cookies = os.environ["wxread"].split("@")
        if len(cookies) > 0:
            logger.info(f"共找到{len(cookies)}个账号 已获取并使用Env环境Cookie")
            logger.info("声明：本脚本为学习python 请勿用于非法用途")
    else:
        logger.info("【提示】变量格式: authtoken=eyJ0eXAiOiJKV1QiLCJhbxxxxx; snapshot=0\n环境变量添加: wxread")
        exit(3)
except Exception as e:
    logger.error(f"发生错误：{e}")
    exit(3)


# -------------------------分割线------------------------
class miniso:
    @staticmethod
    def setHeaders(i):
        headers = {
            "X-Requested-With": "com.tencent.mm",
            "Content-Type": "application/json",
            'Referer': 'https://umm92ibf7ldw99lk-1318684421.cos.ap-nanjing.myqcloud.com/',
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; V2203A Build/SP1A.210812.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5197 MMWEBSDK/20230405 MMWEBID/9296 MicroMessenger/8.0.35.2360(0x2800235D) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Cookie": cookies[i],
        }
        return headers

    @staticmethod
    def geturl(headers):
        try:
            url = f'http://nqyt2plpvv.qqaas.fun/app/read/get'
            response = requests.get(url=url, headers=headers)
            result = response.json()
            id = re.search(r'u=(\w+)', result['data']['location']).group(1)
            res = f"获取阅读url: 成功"
            logger.info(res)
            log_list.append(res)
            time.sleep(5)
            miniso.doRead(headers, id)
        except Exception as e:
            print(e)

    @staticmethod
    def doRead(headers, id):
        try:
            url = f'https://sss.mvvv.fun/app/task/doRead?u={id}&type=1'
            response = requests.get(url=url, headers=headers)
            result = response.json()
            if result['data']['taskKey'] is not None:
                taskKey = result['data']['taskKey']
                res = f"获取参数: 成功"
                logger.info(res)
                log_list.append(res)
                time.sleep(8)
                miniso.Read(headers, id, taskKey)
            else:
                res = f"获取参数: 获取阅读参数失败！"
                logger.info(res)
                log_list.append(res)
        except Exception as e:
            print(e)

    @staticmethod
    def Read(headers, id, taskKey):
        try:
            url = f'https://sss.mvvv.fun/app/task/doRead?u={id}&type=1&key={taskKey}'
            response = requests.get(url=url, headers=headers)
            result = response.json()
            if result['data']['detail'] == '检测中':
                miniso.doRead(headers, id)
            elif result['code'] == 0 and result['data']['taskKey'] is not None:
                taskKey = result['data']['taskKey']
                sleeptime = random.randint(8, 12)
                res = f"阅读: {result['data']['detail']} -- 随机等待{sleeptime}秒后继续...."
                logger.info(res)
                time.sleep(sleeptime)
                miniso.Read(headers, id, taskKey)
            else:
                res = f"阅读: 没获取到文章id,可能本轮阅读已完成 或 此账号已被限制!"
                logger.info(res)
                log_list.append(res)
        except Exception as e:
            print(e)

    @staticmethod
    def my(headers):
        try:
            url = f'http://qmctk1sfcw.qqaas.fun/app/user/myInfo'
            response = requests.get(url=url, headers=headers)
            return response.json()
        except Exception as e:
            print(e)

    @staticmethod
    def myPickInfo(headers):
        try:
            url = f'http://qmctk1sfcw.qqaas.fun/app/user/myPickInfo'
            response = requests.get(url=url, headers=headers)
            return response.json()
        except Exception as e:
            print(e)

    @staticmethod
    def pickAuto(headers, sign):
        try:
            data = sign
            url = 'http://mhxbn1se67.qqaas.fun/app/user/pickAuto'
            response = requests.post(url, headers=headers, data=data)
            if result['code'] == 0:
                res = f"提现: 拔毛成功！"
                logger.info(res)
                log_list.append(res)
            else:
                res = f"提现: {result['msg']}"
                logger.info(res)
                log_list.append(res)
        except Exception as e:
            print(e)

def encrypt(plaintext):
    key = b'5e4332761103722eb20bb1ad53907c6e'
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return b64encode(ciphertext).decode()

if __name__ == '__main__':
    log_list = []  # 存储日志信息的全局变量
    for i in range(len(cookies)):
        head = f"\n------------开始第[{i + 1}]个账号------------"
        logger.info(head)
        log_list.append(head)
        headers = miniso.setHeaders(i)

        result = miniso.my(headers)
        if result['code'] == 0:
            res = f"账号: {result['data']['nameNick']} 今日已读:{result['data']['completeTodayCount']}次 金币:{result['data']['goldNow']}"
            logger.info(res)
            log_list.append(res)
            if result['data']['remainSec'] == 0:
                miniso.geturl(headers)
            else:
                res = f"状态: 距离下次阅读还需{result['data']['remainSec']//60}分钟"
                logger.info(res)
                log_list.append(res)
            if result['data']['goldNow'] > 4000:
                result = miniso.myPickInfo(headers)
                data = result['data']['goldNow']
                body = f'{{"moneyPick":{data:.1f}}}'
                sign = encrypt(body)
                miniso.pickAuto(headers,sign)
        else:
            res = f"账号: {result['msg']}"
            logger.info(res)
            log_list.append(res)

    logger.info("\n============== 推送 ==============")
    send("微信阅读", '\n'.join(log_list))
