import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from DAL import Dhttpbase

class ConfigHttp():
    def __init__(self, mhttpbase):
        self.mhttpbase = mhttpbase
        self.mh = Dhttpbase.ConfigHttp(self.mhttpbase)
    def get(self, api_host,request_url, headers):
       return self.mh.get(api_host,request_url, headers)
    def post(self, api_host,request_url, headers, data):
        return self.mh.post(api_host,request_url, headers, data)
    # def check_param(self):
