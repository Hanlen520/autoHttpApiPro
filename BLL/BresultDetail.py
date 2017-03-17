import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from DAL import DresultDetail

def resultInfo(mresulinfot, **kwargs):
    return DresultDetail.resultInfo(mresulinfot, **kwargs)