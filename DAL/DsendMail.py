
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib,os

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
def new_report(resuleDir):
    lists = os.listdir(resuleDir)
    lists.sort(key=lambda fn: os.path.getmtime(resuleDir + "\\" + fn))
    file_new = os.path.join(resuleDir, lists[-1])
    return file_new
def send_mail(Memail):
    from_addr = Memail.mail_user
    password = Memail.mail_pass
    smtp_server =Memail.mail_host


    msg = MIMEMultipart('related')
    testReportDir='./Report/'
    file=new_report(testReportDir)
    sendfile=open(file, 'rb').read()
    msg['From'] = _format_addr('测试组<%s>' % from_addr)
    msg['To'] = _format_addr('全员<%s>' % Memail.to_addr)
    msg['Subject'] = Header(Memail.headerMsg, 'utf-8').encode()

    msg.attach(MIMEText(open(file, 'rb').read(), 'plain', 'utf-8'))
    part = MIMEApplication(open(file, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename='InterfaceTestReport.xlsx')
    msg.attach(part)

    server = smtplib.SMTP_SSL(smtp_server, Memail.port)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, Memail.to_addr, msg.as_string())
    server.quit()