import sys,os,xlrd
BASE_DIR=os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)
from xml.etree import ElementTree as ET

def getXML(xml, mhttp):
    tree  = ET.parse(xml)
    root = tree.getroot()
    i_base = {}
    interfaceName = []
    i_base["title"] = mhttp.title = root.find("title").text
    i_base["host"] = mhttp.host = root.find("host").text
    i_base["port"] = mhttp.port = root.find("port").text
    i_base["No"] = mhttp.No = root.find("No").text
    mhttp.header = root.find("header").text
    interfaceName.append(i_base)
    for elem in root.findall("InterfaceList"):
        i_app = {"param":[]}
        i_app["id"] = elem.find('id').text
        i_app["name"] = elem.find('name').text
        i_app["method"] = elem.find('method').text
        i_app["url"] = elem.find('url').text
        i_app["hope"] = elem.find('hope').text
        i_app["login"] = elem.find('login').text
        i_app["isList"] = elem.find('isList').text
        i_app["params"] = elem.find('params').text

        # interfaceName.append(i_app)
        # for p in elem.findall("params"):
        #     param = {}
        #     param["name"] = p.find("name").text
        #     param["type"] = p.find("name").attrib.get("type")
        #     param["value"] = p.find("value").text
        #     param["must"] = p.find("must").text
        #     i_app["param"].append(param)
        # interfaceName.append(i_app)
    # print(interfaceName)
    return interfaceName, mhttp
def getExcel(excel, mhttp):
    testCaseFile='TestCase/testYesApi.xlsx'
    testCaseFile = os.path.join(os.getcwd(), testCaseFile)
    # if not os.path.exists(testCaseFile):
    #     logging.error('测试用例文件不存在！')
    #     sys.exit()
    testCase = xlrd.open_workbook(testCaseFile)
    table = testCase.sheet_by_index(0)
    s = None
    for i in range(1, table.nrows):
        if table.cell(i, 8).value.replace('\n', '').replace('\r', '')!= 'yes':
            continue
        # mhttp.num = str(int(table.cell(i, 0).value)).replace('\n', '').replace('\r', '')
        mhttp.api_host= table.cell(i, 2).value.replace('\n', '').replace('\r', '')
        mhttp.request_url = table.cell(i, 3).value.replace('\n', '').replace('\r', '')
        mhttp.request_method = table.cell(i,4).value.replace('\n', '').replace('\r', '')
        mhttp.request_data_type = table.cell(i,5).value.replace('\n', '').replace('\r', '')
        mhttp.request_data = table.cell(i,6).value.replace('\n', '').replace('\r', '').encode('utf-8')
        mhttp.check_point = table.cell(i,7).value.replace('\n', '').replace('\r', '')
    i_base = {}
    interfaceName = []
    return interfaceName, mhttp
# def runTest(testCaseFile):
#     testCaseFile = os.path.join(os.getcwd(), testCaseFile)
#     testCase = xlrd.open_workbook(testCaseFile)
#     table = testCase.sheet_by_index(0)
#     errorCase = []  # 用于保存接口返回的内容和HTTP状态码
#     s = None
#     for i in range(1, table.nrows):
#         if table.cell(i, 8).value.replace('\n', '').replace('\r', '')!= 'yes':
#             continue
#         num = str(int(table.cell(i, 0).value)).replace('\n', '').replace('\r', '')
#         api_host= table.cell(i, 2).value.replace('\n', '').replace('\r', '')
#         request_url = table.cell(i, 3).value.replace('\n', '').replace('\r', '')
#         request_method = table.cell(i,4).value.replace('\n', '').replace('\r', '')
#         request_data_type = table.cell(i,5).value.replace('\n', '').replace('\r', '')
#         request_data = table.cell(i,6).value.replace('\n', '').replace('\r', '').encode('utf-8')
#         check_point = table.cell(i,7).value.replace('\n', '').replace('\r', '')
#
#
#         status, resp, s = interfaceTest(num, api_host, request_url, request_data, check_point,
#                                         request_method, request_data_type, s)
#         if status != 200 or check_point not in resp:  # 如果状态码不为200或者返回值中没有检查点的内容，那么证明接口产生错误，保存错误信息。
#             errorCase.append((num + ' ' + request_url, str(status), 'http://' + api_host + request_url, resp))
#     return errorCase

# def interfaceTest(num, api_host, request_url, request_data, check_point,
#                                         request_method, request_data_type, s=None):
#         headers = {
#             "Accept": "application/json, text/plain, */*",
#             "Authorization": "bearer cWlxaTE6ZDZiMTlkZmMtOGU1ZS00MTBiLTk0ZGYtODUwZDk3MWMzZDVk",
#             "Content-Type": "application/json;charset=UTF-8",
#             "Referer": "http://172.168.101.83/",
#             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
#         }
#         if s == None:
#             s = requests.session()
#         if request_method == 'post':
#             if request_url != '/auth/login':
#                 r = s.post(url='http://' + api_host + request_url, data=request_data,
#                        headers=headers)
#             elif request_url == '/auth/login':
#                 # s = requests.session()
#                 r = s.post(url= 'http://' +  api_host + request_url, data=request_data,
#                        headers={'Content-Type': 'application/json;charset=UTF-8'})  # 由于登录密码不能明文传输，采用MD5加密，在之前的代码中已经进行过json.loads()转换，所以此处不需要解码
#         elif  request_method == 'get':
#                 r = s.get(url='http://' + api_host + request_url,
#                        headers=headers)
#         else:
#             logging.error(num + ' ' + request_url + '  HTTP请求方法错误，请确认[Request Method]字段是否正确！！！')
#             s = None
#             return 400,  s
#         status = r.status_code
#         resp = r.text
#         demo=re.search(check_point, str(r.text))
#         if status == 200:
#             if re.search(check_point, str(r.text)):
#                 logging.info(num + ' ' + request_url + ' 成功，' + str(status) + ', ' + str(r.text))
#                 return status, resp, s
#             else:
#                 logging.error(num + ' ' + request_url + ' 失败！！！，[' + str(status) + '], ' + str(r.text))
#                 return 200, resp, None
#         else:
#                 logging.error(num + ' ' + request_url + '  失败！！！，[' + str(status) + '],' + str(r.text))
#                 return status, resp.decode('utf-8'), None
#
