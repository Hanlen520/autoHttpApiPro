import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from DAL import Dresult
def result(mresult, **kwargs):
    return Dresult.result(mresult, **kwargs)