import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
import configparser
from schematics.models import Model
from schematics.types import StringType, URLType
from schematics.types.compound import MultiType,ListType
# BaseHttp类

class BaseHttp(Model):
    '''配置要测试接口服务器的ip、端口、域名等信息'''
    host = StringType()
    port = StringType()
    No = StringType()
    header = StringType()



