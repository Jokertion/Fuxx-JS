#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: jokertion
@file: shikee_login.py
@time: 2020/2/29 21:39
@desc: 
"""
import requests
import execjs
import time

name, password = 'login_name', 'login_password'
session = requests.Session()


def get_time():
    t = int(round(time.time() * 1000))
    return t


def encrypt(pwd):
    file = open('shikee.js').read()
    pwd = execjs.compile(file).call('gen_rsa_pwd', pwd)
    return pwd


def login():
    url = 'http://login.shikee.com/check/?&_{}'.format(get_time())
    data = {
        'username': name,
        'password': encrypt(password),
        'vcode': '',
        'to': 'http://www.shikee.com/'
    }
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://login.shikee.com',
        'Referer': 'http://login.shikee.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    resp = session.post(url, data=data, headers=headers).json()
    print(resp)

    url2 = 'http://login.shikee.com/success/?to=http%3A%2F%2Fwww.shikee.com%2F'
    resp2 = session.get(url2)
    print(resp2.text)


if __name__ == '__main__':
    login()
