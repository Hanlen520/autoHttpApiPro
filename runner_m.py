import sys,os
BASE_DIR=os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
import unittest
import time
from COMMON.BaseGoals import Goals as go
from COMMON import check
import xlsxwriter
from model import Memail
from BLL import BgetEmail,BsendEmail
from BLL import BexcelReport as excel
from COMMON import operateXML as om
from BLL import Bhttpbase
from model import Mhttpbase
from BLL import Bresult, BresultDetail
from model import Mresult, MresultDetail
from COMMON import http_param
import json
import ast
import hashlib,requests,json,re
import configparser,logging,xlrd
import  HTMLTestRunner
from email.mime.text import MIMEText
from email.header import Header
import  smtplib

#===========================================生成日志===============================================================================
log_file = os.path.join(os.getcwd(),'log/yesLog.log')
log_format = '[%(asctime)s] [%(levelname)s] %(message)s'     #配置log格式
logging.basicConfig(format=log_format, filename=log_file, filemode='w', level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_format)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#======================================获取邮件配置文件===============================================================================
def get_email():
    g_email = Memail.email()
    g_email.file = "email.ini"
    email = BgetEmail.read_email(g_email)
    return email
#======================================测试报告的输出===============================================================================
def excel_report(wd, data, worksheet_init, worksheet_detail):
    ex = excel.ExcelReport(wd, data)
    ex.init(worksheet_init, data[0])
    ex.detail(worksheet_detail, data[1])
#======================================得到excel配置接口信息和http请求实体类===============================================================================
def get_api():
    return om.getExcel("test",Mhttpbase.BaseHttp())
#=====================================设置http请求实体类==============================================================================
def configHttp(httpbase):
   return Bhttpbase.ConfigHttp(httpbase)
#=====================================接口详情页的excel==============================================================================
def resultInfo(mresultinfo, **kwargs):
    return BresultDetail.resultInfo(mresultinfo, **kwargs)
#=====================================接口初始页的excel==============================================================================
def result(mresult, **kwargs):
    return Bresult.result(mresult, **kwargs)
#=====================================错误日志统计=================================================================================
def sum_test_data(flag):
    if flag:
        go.RESULT = 'Pass'
        go.SUCCESS_SUM += 1
    else:
        go.RESULT = 'Fail'
        go.ERROR_NUM += 1
#=====================================读取http参数  测试结果定义 =================================================================================
httpbase = get_api()
mresult = Mresult.result()
mresult.info = []
#=====================================测试用例(组)类 =================================================================================
class TestInterfaceCase(unittest.TestCase):
    def __init__(self, num,name,api_host, request_url,request_method, request_data,check_point):
        super(TestInterfaceCase, self).__init__('function')
        self.num=num
        self.name = name
        self.api_host = api_host
        self.request_url = request_url
        self.request_method = request_method
        self.request_data = request_data
        self.check_point = check_point
    def setUp(self):
        self.config_http = configHttp(httpbase)
    def function(self):
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": "bearer cWlxaTE6ZDZiMTlkZmMtOGU1ZS00MTBiLTk0ZGYtODUwZDk3MWMzZDVk",
        }
        temp_result = False
        resultFlag="失败"
        if self.request_method == "post":
            go.REALLY_RESULT = self.config_http.post(self.api_host,self.request_url, headers, self.request_data)
        if self.request_method == 'post':
            if self.request_url != '/auth/login':
                go.REALLY_RESULT = self.config_http.post(api_host=self.api_host, request_url=self.request_url,data=self.request_data, headers=headers)
            elif self.request_url == '/auth/login':
                go.REALLY_RESULT = self.config_http.post(api_host=self.api_host, request_url=self.request_url,data=self.request_data, headers={'Content-Type': 'application/json;charset=UTF-8'})
        elif  self.request_method == 'get':
                go.REALLY_RESULT = self.config_http.get(api_host=self.api_host, request_url=self.request_url, headers=headers)
        else:
            logging.error(self.num + ' ' + self.request_url + '  HTTP请求方法错误，请确认[Request Method]字段是否正确！！！')
        status = go.REALLY_RESULT["status_code"]
        resp = go.REALLY_RESULT
        check_point=self.check_point
        request_data=self.request_data
        if status == 200:
            if re.search(self.check_point, str(go.REALLY_RESULT)):
                temp_result=True  # 统计
                resultFlag="成功"
                logging.info(self.num + ' ' + self.request_url + ' 成功，' + str(status) + ', ' + str(go.REALLY_RESULT))
            else:
                temp_result=False
                resultFlag="失败"
                logging.error(self.num + ' ' + self.request_url + ' 失败！！！，[' + str(status) + '], ' + str(go.REALLY_RESULT))
        else:
            temp_result = False
            resultFlag = "失败"
            logging.error(self.num + ' ' + self.request_url + '  失败！！！，[' + str(status) + '],' + str(go.REALLY_RESULT))
        sum_test_data(temp_result)
        go.CASE_TOTAL += 1
        mresult.info.append(json.loads(json.dumps(resultInfo(MresultDetail.resultInfo(), t_id=self.num, t_name=self.name, t_url=self.request_url,t_param=self.request_data.decode("utf-8"), t_actual=json.dumps(resp).encode().decode('unicode-escape'), t_hope=self.check_point, t_result=resultFlag,t_method=self.request_method).to_primitive())))
#=====================================获取测试套件 =================================================================================
def get_test_suite(num,name,api_host, request_url,request_method, request_data,check_point):
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestInterfaceCase(num=num,name=name,api_host=api_host, request_url=request_url,request_method=request_method, request_data=request_data,check_point=check_point))
    return test_suite
#=====================================运行测试用例函数 =================================================================================
def run_case(runner):
    testCaseFile='TestCase\\testYesApi.xlsx'
    testCaseFile = os.path.join(os.getcwd(), testCaseFile)
    if not os.path.exists(testCaseFile):
        logging.error('测试用例文件不存在！')
        sys.exit()
    testCase = xlrd.open_workbook(testCaseFile)
    table = testCase.sheet_by_index(0)
    errorCase = []  # 用于保存接口返回的内容和HTTP状态码
    s = None
    for i in range(1, table.nrows):
        if table.cell(i, 8).value.replace('\n', '').replace('\r', '')!= 'yes':
            continue
        num = str(int(table.cell(i, 0).value)).replace('\n', '').replace('\r', '')
        name = table.cell(i, 1).value.replace('\n', '').replace('\r', '')
        api_host= table.cell(i, 2).value.replace('\n', '').replace('\r', '')
        request_url = table.cell(i, 3).value.replace('\n', '').replace('\r', '')
        request_method = table.cell(i,4).value.replace('\n', '').replace('\r', '')
        request_data_type = table.cell(i,5).value.replace('\n', '').replace('\r', '')
        request_data = table.cell(i,6).value.replace('\n', '').replace('\r', '').encode('utf-8')
        check_point = table.cell(i,7).value.replace('\n', '').replace('\r', '')
        test_suite = get_test_suite(num=num,name=name,api_host=api_host, request_url=request_url,request_method=request_method, request_data=request_data,check_point=check_point)
        runner.run(test_suite)

def getNowTime():
    return time.strftime("%Y-%m-%d %H_%M_%S", time.localtime(time.time()))
#=====================================运行测试套件 =================================================================================
if __name__ == '__main__':
    start_time = time.time()
    runner = unittest.TextTestRunner()
    run_case(runner)
    end_time = time.time()
    sum_time = "%.2f" % (end_time - start_time)
    # 测试报告
    testReportDir='./Report/'
    filename = testReportDir+getNowTime()+'report.xlsx'
    fp = open(filename,'wb')
    workbook = xlsxwriter.Workbook(fp)
    worksheet = workbook.add_worksheet("测试总况")
    worksheet2 = workbook.add_worksheet("测试详情")
    data = json.loads(json.dumps(result(mresult, test_date=str(sum_time) + "毫秒", test_sum=go.CASE_TOTAL, test_failed=go.ERROR_NUM, test_version="v1.0", test_pl="python3",
    test_net="83环境", test_name="优胜教育后台接口", test_success=go.SUCCESS_SUM, info=mresult.info)))
    excel_report(workbook, data, worksheet, worksheet2)
    # 发送email
    # get_email = get_email()
    # BsendEmail.send_mail(get_email)



