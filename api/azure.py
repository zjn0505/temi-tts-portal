# -*- coding: UTF-8 -*-
import requests # Command to install: `pip install requests`

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlsplit, parse_qs
from xml.dom import minidom

import os



voices = {
    "EN_US":("en-US-JennyNeural", "en-US-GuyNeural"),
    "ZH_CN":("zh-CN-XiaoxiaoNeural", "zh-CN-YunyangNeural"),
    "ZH_HK":("zh-HK-HiuGaaiNeural", "zh-HK-WanLungNeural"),
    "ZH_TW":("zh-TW-HsiaoChenNeural", "zh-TW-YunJheNeural"),
    "TH_TH":("th-TH-PremwadeeNeural", "th-TH-NiwatNeural"),
    "HE_IL":("he-IL-HilaNeural", "he-IL-AvriNeural"),
    "KO_KR":("ko-KR-SunHiNeural", "ko-KR-InJoonNeural"),
    "JA_JP":("ja-JP-NanamiNeural", "ja-JP-KeitaNeural"),
    "IN_ID":("id-ID-GadisNeural", "id-ID-ArdiNeural"),
    "ID_ID":("id-ID-GadisNeural", "id-ID-ArdiNeural"),
    "DE_DE":("de-DE-KatjaNeural", "de-DE-ConradNeural"),
    "FR_FR":("fr-FR-DeniseNeural", "fr-FR-HenriNeural"),
    "FR_CA":("fr-CA-SylvieNeural", "fr-CA-AntoineNeural"),
    "PT_BR":("pt-BR-FranciscaNeural", "pt-BR-AntonioNeural"),
    "AR_EG":("ar-EG-SalmaNeural", "ar-EG-ShakirNeural"),
    "AR_AE":("ar-EG-SalmaNeural", "ar-EG-ShakirNeural"),
    "AR_XA":("ar-EG-SalmaNeural", "ar-EG-ShakirNeural"),
    "RU_RU":("ru-RU-SvetlanaNeural", "ru-RU-DmitryNeural"),
    "IT_IT":("it-IT-ElsaNeural", "it-IT-DiegoNeural"),
    "PL_PL":("pl-PL-AgnieszkaNeural", "pl-PL-MarekNeural"),
    "ES_ES":("es-ES-ElviraNeural", "es-ES-AlvaroNeural")
}

def getHeader():
    headers = {'Ocp-Apim-Subscription-Key': os.environ['Ocp_Apim_Subscription_Key']}
    return headers

def requestTts(text, name, speed, pitch, gender):

    print (text, name, speed, pitch, gender)

    if gender == 'true':
        voice = voices[name][0]
    else:
        voice = voices[name][1]


    print (voice)
        
    # **** Send the request *****
    requestUrl = 'https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issueToken'

    ## 使用requests.session保持长连接
    session = requests.session()
    session.headers.update(getHeader())

    r = session.post(requestUrl)

    # print 'Response...'
    print ('HTTP Status Code:%d' % r.status_code)
    print (r.text)
    token = r.text

    requestUrl = 'https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1'
    session2 = requests.session()
    session2.headers.update({'Authorization': 'Bear ' + token, 'X-Microsoft-OutputFormat':'audio-16khz-64kbitrate-mono-mp3', 'Content-Type': 'application/ssml+xml'})

    root = minidom.Document()
  
    xml = root.createElement('speak') 
    xml.setAttribute('version', '1.0')
    xml.setAttribute('xml:lang', 'en-US')
    root.appendChild(xml)
    
    voiceChild = root.createElement('voice')
    voiceChild.setAttribute('name', voice)
    
    xml.appendChild(voiceChild)

    prosodyChild = root.createElement('prosody')
    prosodyChild.setAttribute('rate', speed)
    prosodyChild.setAttribute('pitch', str(pitch) + "%")
    voiceChild.appendChild(prosodyChild)

    textNode = root.createTextNode(text)
    prosodyChild.appendChild(textNode)
    
    xml_str = root.toprettyxml()

    print (xml_str)

    r = session2.post(requestUrl, data = xml_str)

    # print 'Response...'
    print ('HTTP Status Code:%d' % r.status_code)
    return r.content


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(self.path)
        params = parse_qs(urlsplit(self.path).query)
        print(urlsplit(self.path).query)
        self.send_response(200)
        self.send_header('Content-type', 'audio/mpeg')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(requestTts(params["text"][0], params["name"][0], params["speed"][0], params["pitch"][0], params["gender"][0]))
        return

"""
curl --request POST \
  'https://texttospeech.googleapis.com/v1beta1/text:synthesize?key=' \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --data '{"input":{"text":"Hello"},"voice":{"languageCode":"ja-JP","name":"ja-JP-Wavenet-A","ssmlGender":"FEMALE"},"audioConfig":{"audioEncoding":"OGG_OPUS"}}' \
  --compressed


"""