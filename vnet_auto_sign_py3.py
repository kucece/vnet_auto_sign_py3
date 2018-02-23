#! /usr/bin/env python
# coding:utf-8

import requests
import os
import execjs
import logging
import json
import time
import sys
from js import execjs
class UnicomSign:

    login_header = {
        'User-Agent': 'Mozilla/5.0 (Linux; HFWSH_USER Android 7.0; SM-G9350 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36'}
    signin_header = {
        'User-Agent': 'Mozilla/5.0 (Linux; HFWSH_USER Android 7.0; SM-G9350 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
        'X-Requested-With': 'com.ailk.main.flowassistant', 
		'Content-Length': 0, 
		'Origin': 'https://ll.fj10010.com/',
        'Referer': 'https://ll.fj10010.com/faWapNew/login/login.html?url=https://ll.fj10010.com/faWap/myFlow!index.action'}
    phone = ''
    pwd = ''
    phone_encode = ''
    pwd_encode = ''
    cookie = None
    cookieFile = './cookie.dat'
    ctx = None
    enctyptedParam = ''

    
    def loadJs(self,path):
        if not os.path.exists(path):
            logging.info(time.ctime() + "file no exist %s %r" + path)
            return
        f = open(path, 'r')
        line = f.readline()
        jsstr = ''
        while line:
            jsstr = jsstr + line
            line = f.readline()
        self.ctx = execjs.compile(jsstr.encode("utf-8"))
        
    def rsaEnctytedString(self,param):
        
        postdata={}
        resp = self.s.post(url='https://ll.fj10010.com/login!keyPair.action', params=postdata, headers=self.login_header)
        
        data = json.loads(resp.text)
        exponent = data["modulus"]["exponent"]
        modulus = data["modulus"]["modulus"]
        if param.strip() :
            print( self.ctx.call('add',2,2))
            return self.ctx.call('rsaEnctytedString',exponent, modulus, param)
        else:
            return param
        
    def __init__(self, username, pwd, logType):
        self.phone = username
        self.pwd = pwd
        self.logType = logType
        self.s = requests.Session()
        paths = os.path.dirname(__file__)
        dir = paths + "./js/security.js"
        self.loadJs(dir)
        self.phone_encode = self.rsaEnctytedString(self.phone)
        self.pwd_encode = self.rsaEnctytedString(self.pwd)

        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename="auto_sign.log",
                            filemode='a')

        
    def login(self):
        print ('login...')
        
        postdata = {'loginName': self.phone_encode, 'code': self.pwd_encode, 'logType': '3'}       
        resp =  self.s.post(url='https://ll.fj10010.com/faWap/faLogin!login.action', params=postdata, headers=self.login_header)
        result =resp.text
        if result.find(u'签到有礼') != -1:
            logging.info(time.ctime() + "登入成功")
            print ('Login successfully!')
        else:
            logging.info(time.ctime() + "登入失败")
            print ('Login failed due to Email or Password error...')
            sys.exit()

    def signIn(self):
        postdata={}
        print ('signing...')
        resp =  self.s.post(url='https://ll.fj10010.com/app/sign!sign.action', params=postdata, headers=self.login_header)
        result = resp.text
        data = json.loads(result)
        if data['code'] == '0000':
            print (self.phone,'have signed', 'signDay',data['signDay'],  'todayNum:',data['todayNum'],'signList',data['signList'])
            logging.info(time.ctime() +' phoneNo:'+ self.phone + '  have signed signDay:' + data['signDay'] + '  todayNum:' + data['todayNum'] + '  signList:' + data['signList'])
        else:
            print ('signing failed code:', data['code'],'错误消息:',data['msg'])
            logging.info(time.ctime() + ' signing failed code:'+ data['code'] + '错误消息:' + data['msg'])

if __name__ == '__main__':
    user = UnicomSign('phoneNum', 'psw',3)
    user.login()

    user.signIn()
    logging.info(time.ctime() + '---------------------------执行完毕---------------------------')
    logging.shutdown()
