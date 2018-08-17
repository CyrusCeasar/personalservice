import json

RESULT_SUCCESS = "0"
RESULT_FAILED = "-1"
ERROR_PARAM_WRONG = "参数错误"
ERROR_PARAM_MISS = "缺少参数"
ERROR_SERVER_DOWN = "服务器异常"


class Result:
    result_code = RESULT_FAILED
    result_msg = ERROR_PARAM_WRONG

    def __init__(self, code, msg):
        self.result_code = code
        self.result_msg = msg

    def __str__(self):
        print(self.result_code + "---" + self.result_msg)

    def getJsonStr(self, obj=None):
        dict = {'result_msg': self.result_msg, 'result_code': self.result_code, 'data': obj}
        return dict
