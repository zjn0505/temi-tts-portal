# -*- coding: UTF-8 -*-
import requests # Command to install: `pip install requests`

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlsplit, parse_qs

import os

# ***** Task 1: 拼接请求数据和时间戳 *****

def getHeader(postData):
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    return headers

def requestTts(text, name):
    ## 获取请求数据(也就是HTTP请求的Body)

    print(name)
    languageCode = name.split('-')[0] + '-' +  name.split('-')[1]
    print(languageCode)

    postDataTts = '{"input":{"text":"'+ text +'"},"voice":{"languageCode":"'+languageCode+'","name":"'+name+'","ssmlGender":"FEMALE"},"audioConfig":{"audioEncoding":"OGG_OPUS"}}'

    print(postDataTts)
    # **** Send the request *****
    requestUrl = 'https://texttospeech.googleapis.com/v1beta1/text:synthesize?key=' + os.environ['GOOGLE_API_KEY']


    ## 使用requests.session保持长连接
    session = requests.session()
    session.headers.update(getHeader(postDataTts))

    r = session.post(requestUrl, data = postDataTts.encode("utf-8"))

    # print 'Response...'
    print ('HTTP Status Code:%d' % r.status_code)
    print (r.text)
    return r.text


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        params = parse_qs(urlsplit(self.path).query)
        print(urlsplit(self.path).query)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(requestTts(params["text"][0], params["name"][0]).encode())
        return

"""
curl --request POST \
  'https://texttospeech.googleapis.com/v1beta1/text:synthesize?key=' \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --data '{"input":{"text":"Hello"},"voice":{"languageCode":"ja-JP","name":"ja-JP-Wavenet-A","ssmlGender":"FEMALE"},"audioConfig":{"audioEncoding":"OGG_OPUS"}}' \
  --compressed


"""