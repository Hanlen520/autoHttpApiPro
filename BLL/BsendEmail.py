import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from DAL import DsendMail

def send_mail(email):
    DsendMail.send_mail(email)

