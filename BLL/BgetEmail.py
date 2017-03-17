import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from COMMON import OperateFile as of
from DAL import DgetEmail

def read_email(Memail):
    if of.base_file(Memail.file, 'r').check_file():
        return DgetEmail.read_email(Memail)
    print(u"文件不存在")
    return ""