import requests
import ast
import json

class ConfigHttp():
    def __init__(self, mhttpbase):
        self.mhttpbase = mhttpbase
    def get(self,api_host,request_url, headers):
        result = {}
        r = requests.get(url='http://' + api_host + request_url,headers=headers)
        r.encoding = 'UTF-8'
        if r.status_code == 200:
            result = json.loads(r.text)
        result["status_code"] = r.status_code
        return result

    # 封装HTTP POST请求方法,支持上传图片
    def post(self, api_host,request_url, headers, data):
        result = {}
        r = requests.post(url='http://' + api_host + request_url, data=data,
                   headers=headers)
        r.encoding = 'UTF-8'
        if r.status_code == 200:
            result = json.loads(r.text)
        result["status_code"] = r.status_code
        return   result
