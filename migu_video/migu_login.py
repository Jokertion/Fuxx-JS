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
from migu.migu_pwd import name_pwd
from pprint import pprint

name, password = name_pwd()
HEADERS = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://passport.migu.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}
f = open('migu.js', 'r+', encoding='utf-8')
ctx = execjs.compile(f.read())
session = requests.Session()


def get_enpassword(pwd: str, a: dict) -> str:
    """
    generate params: enpassword
    :param pwd:
    :param a:
    :return:
    """
    enpassword = ctx.call('get_enpassword', pwd, a)
    # print('enpassword: ', enpassword)
    return enpassword


def get_finger_print_finger_print_detail(a: str) -> dict:
    """
    generate paramas:  FingerPrint and FingerPrint
    :return: result: FingerPrint   details: FingerPrint
    """
    fp_dic = ctx.call('get_fingerPrint', a)
    # pprint(fp_dic)
    return fp_dic


def get_login_id(account: str, a: str) -> str:
    """
    generate params: loginID
    :param account:
    :param a:
    :return:
    """
    login_id = ctx.call('get_RsaAccout', account, a)
    # print('login_Id', login_id)
    return login_id


def get_a():
    """
    A request generate public_key and return a.
    The a is required in generating other params,
    including loginID, enpassword, fingerPrint and fingerPrintDetail.

        a = {
        "status": 2000,
        "message": "",
        "header": {},
        "result": {
            "publicExponent": "010001",
            "modulus": "00833c...06817"
        }
    }
    :return: str(a)
    """
    url = 'https://passport.migu.cn/password/publickey'
    response = session.post(url, headers=HEADERS).json()
    # print(response)
    return response


def login(account, pwd, a):
    url = 'https://passport.migu.cn/authn'

    fp_dic = get_finger_print_finger_print_detail(a)
    finger_print = fp_dic.get('details')
    finger_print_detail = fp_dic.get('details')
    data = {
        'sourceID': '208003',
        'appType': '0',
        'relayState': '',
        'loginID': get_login_id(account, a),
        'enpassword': get_enpassword(pwd, a),
        'captcha': '',
        'imgcodeType': '1',
        'rememberMeBox': '1',
        'fingerPrint': finger_print,
        'fingerPrintDetail': finger_print_detail,
        'isAsync': 'true'
    }
    response = session.post(url, headers=HEADERS, data=data)

    print(response.text)


def main():
    try:
        a = get_a()
        login(name, password, a)
        # res:
        # {"status": 2000, "message": "", "header": {"resultcode": "104000"},
        #  "result": {"risk_resultCode": "00000",
        #             "redirectURL": "http://www.migu.cn/user/tokenValidate",
        #             "authNType": "MiguPassport",
        #             "risk_LevelCode": "0",
        #             "risk_ruleCode": "00000000",
        #             "risk_measureCode": "000000",
        #             "token": "STnid0000011583605203343owDDS5sywNY6LafQUsf2QwRqSdcHWumu"}}

    finally:
        f.close()


def test_get_params():
    a = get_a()
    get_enpassword(password, a)
    get_finger_print_finger_print_detail(a)
    get_login_id(name, a)


if __name__ == '__main__':
    # test_get_params()
    main()
