# coding:utf-8
import os
import requests
from common.readexcel import ExcelUtil
class Re_Token:
    def __init__(self):
        curpath = os.path.dirname(os.path.realpath(__file__))
        self.filepath = os.path.join(curpath, "debug_api.xlsx")
        self.s = requests.session()
        self.SheetName = "Sheet1"

    def get_token(self):
        testdata = ExcelUtil(self.filepath,self.SheetName).dict_data()[0]
        method = testdata["method"]
        url = testdata["url"]
        params = testdata["params"]
        headers = eval(testdata["header"])
        type = testdata["type"]
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
        verify = False
        res = self.s.request(method=method,
                          url=url,
                          params=params,
                          headers=headers,
                          json=body,
                          verify=verify
                           )
        token = res.json()["data"]["token"]
        return token

    '''def get_token2():
        url = "http://test.article.yingpiao360.com/api/app/login-pwd"
        header = {
            "Content-Type": "application/json; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; en; VCE-AL00 Api/HUAWEIVCE-AL00) AppleWebKit/534.30 (KHTML, like Gecko) Version/5.0 Mobile Safari/534.30"
        }
        data = json.dumps({
            "phone": "17788780783",
            "userPass": "582057ls"
        })
        s = requests.session()
        login_ret = s.post(url, headers=header, data=data)
        token = login_ret.json()["data"]["token"]
        return token'''
if __name__ == "__main__":
    print(Re_Token().get_token())