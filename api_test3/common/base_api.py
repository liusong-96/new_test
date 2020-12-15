# coding:utf-8
import json
import requests
from common.logger import Log
from common.readexcel import ExcelUtil
from common.writeexcel import copy_excel, Write_excel
from common.re_token import Re_Token

log = Log()
def send_requests(s, testdata):
    '''封装requests请求'''
    print('testdata:',testdata)
    method = testdata["method"]
    url = testdata["url"]
    # url后面的params参数
    try:
        params = eval(testdata["params"])
    except:
        params = None
    # 请求头部headers
    try:
        headers = eval(testdata["header"])
        print("请求头部：%s" % headers)
    except:
        headers = None
    need_token = testdata["need_token"]
    if need_token == "yes":
        token = Re_Token().get_token()
        headers["Bpt-App-Token"] = token
    # post请求body类型
    type = testdata["type"]
    test_nub = testdata['id']
    print("*******正在执行用例：-----  %s  ----**********" % test_nub)
    print("请求方式：%s, 请求url:%s" % (method, url))
    print("请求params：%s" % params)
    # post请求body内容
    try:
        bodydata = eval(testdata["body"])
    except:
        bodydata = {}
    # 判断传data数据还是json
    if type == "data":
        body = bodydata
    elif type == "json":
        body = bodydata
    else:
        body = bodydata
    if method == "post": print("post请求body类型为：%s ,body内容为：%s" % (type, body))
    verify = False
    res = {}   # 接受返回数据
    try:
        r = s.request(method=method,
                      url=url,
                      params=params,
                      headers=headers,
                      json=body,
                      verify=verify
                       )
        print("页面返回信息：%s" % r.content.decode("utf-8"))
        log.info(u'用例标题:%s\n请求地址：%s\n请求方式:%s\n请求正文：%s\n响应头:%s\n响应正文：%s\n' % (test_nub,r.url, r.request.headers, r.request.body, r.headers, r.text))
        res['id'] = testdata['id']
        res['rowNum'] = testdata['rowNum']
        res["statuscode"] = str(r.status_code)  # 状态码转成str
        res["text"] = r.content.decode("utf-8")
        res["times"] = str(r.elapsed.total_seconds())   # 接口请求时间转str
        if res["statuscode"] != "200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
        res["msg"] = ""
        if testdata["checkpoint"] in res["text"]:
            res["result"] = "pass"
            print("用例测试结果:   %s---->%s" % (test_nub, res["result"]))
        else:
            res["result"] = "fail"
        return res
    except Exception as msg:
        res["msg"] = str(msg)
        return res
def wirte_result(result, filename="D:/py_test/new_test/logs/test_result.xlsx"):
    # 返回结果的行数row_nub
    row_nub = result['rowNum']
    # 写入statuscode
    wt = Write_excel(filename)
    wt.write(row_nub, 9, result['statuscode'])       # 写入返回状态码statuscode,第8列
    wt.write(row_nub, 10, result['times'])            # 耗时
    wt.write(row_nub, 11, result['error'])            # 状态码非200时的返回信息
    wt.write(row_nub, 13, result['result'])           # 测试结果 pass 还是fail
    wt.write(row_nub, 14, result['msg'])           # 抛异常
if __name__ == "__main__":
    data = ExcelUtil("debug_api.xlsx").dict_data()
    s = requests.session()
    res = send_requests(s, data[0])
    copy_excel("debug_api.xlsx", "D:/py_test/api_test3/logs/test_result.xlsx")
    wirte_result(res, filename="D:/py_test/api_test3/logs/test_result.xlsx")