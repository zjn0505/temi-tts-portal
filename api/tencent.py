# -*- coding: UTF-8 -*-
import datetime, hashlib, hmac
import requests # Command to install: `pip install requests`

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlsplit, parse_qs

import os

# ***** Task 1: 拼接请求数据和时间戳 *****

def getHeader(postData):
    ## 获得ISO8601时间戳
    credentialDate = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

    ## 拼接数据
    signingContent = postData + credentialDate

    # ***** Task 2: 获取Signature签名 *****
    signature = hmac.new(bytes(os.environ['ACCESS_TOKEN'] , 'utf-8'), bytes(signingContent, encoding='utf-8'), hashlib.sha256).hexdigest()

    # ***** Task 3: 在HTTP请求头中带上签名信息
    authorizationHeader = 'TVS-HMAC-SHA256-BASIC' + ' ' + 'CredentialKey=' + os.environ['APP_KEY'] + ', ' + 'Datetime=' + credentialDate + ', ' + 'Signature=' + signature

    headers = {'Content-Type': 'application/json; charset=UTF-8', 'Authorization': authorizationHeader}

    return headers

def requestRichAnswer():

    ## 获取请求数据(也就是HTTP请求的Body)
    postDataRichAnswer = '{"header": {"guid": "{{STRING}}","qua": "{{STRING}}","user": {"user_id": "{{STRING}}"},"lbs": {"longitude": 1.1111,"latitude": 2.2222},"ip": "8.8.8.8"},"payload": {"query": "你叫什么名字"}}'

    # **** Send the request *****
    requestUrl = 'https://aiwx.html5.qq.com/api/v1/richanswer'

    # print 'Begin request...'
    # print 'Request Url = ' + requestUrl

    ## 使用requests.session保持长连接
    session = requests.session()
    session.headers.update(getHeader(postDataRichAnswer))
    # print 'Request Headers =' + str(session.headers)

    r = session.post(requestUrl, data = postDataRichAnswer)

    # print 'Response...'
    # print 'HTTP Status Code:%d' % r.status_code
    # print r.text
    return r.text


def requestTts(text):
    ## 获取请求数据(也就是HTTP请求的Body)
    postDataTts = '{"header": {"guid": "{{STRING}}","qua": "{{STRING}}","user": {"user_id": ""},"lbs": {"longitude": 132.56481,"latitude": 22.36549},"ip": "8.8.8.8","device": {"network": "4G"}},"payload": {"speech_meta": {"compress": "MP3","person": "YEZI","volume": 50,"speed": 50,"pitch": 50},"session_id": "{{STRING}}","index": 0,"single_request": true,"content": {"text": "'+ text +'"}}}'

    print(postDataTts)
    # **** Send the request *****
    requestUrl = 'https://aiwx.html5.qq.com/api/tts'

    # print 'Begin request...'
    # print 'Request Url = ' + requestUrl

    ## 使用requests.session保持长连接
    session = requests.session()
    session.headers.update(getHeader(postDataTts))
    # print 'Request Headers =' + str(session.headers)

    r = session.post(requestUrl, data = postDataTts.encode("utf-8"))

    # print 'Response...'
    print ('HTTP Status Code:%d' % r.status_code)
    print (r.text)
    return r.text

# requestRichAnswer()
# requestTts()

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        params = parse_qs(urlsplit(self.path).query)
        print(urlsplit(self.path).query)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(requestTts(params["text"][0]).encode())
        return