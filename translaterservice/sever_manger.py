import os
import subprocess

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utils import *

UTF_8 = 'utf-8'


def get_vps_cache_usage():
    result = subprocess.run(['free', '-h'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
    return result


class ServerView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def hello_world():
        return Response(Result(RESULT_SUCCESS, "成功获取").get_json_str())

    @staticmethod
    def get_mem_usage():
        return Response(Result(RESULT_SUCCESS, "成功获取").get_json_str(get_vps_cache_usage()))

    @staticmethod
    def get_cpu_usage():
        result = subprocess.run(['mpstat'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
        return Response(Result(RESULT_SUCCESS, "成功获取").get_json_str(result))

    @staticmethod
    def ps(self):
        result = subprocess.run(['ps', '-ejf'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
        return Response(Result(RESULT_SUCCESS, "成功获取").get_json_str(result))

    @staticmethod
    def last(self):
        result = os.popen('last | grep "logged in"').read().splitlines()
        return Response(Result(RESULT_SUCCESS, "成功获取").get_json_str(result))

    @staticmethod
    def df(self):
        result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
        return Response(Result(RESULT_SUCCESS, "成功获取").get_json_str(result))

    def get(self, request):
        t = request.GET.get('type')
        if t == 'cpu':
            return self.get_cpu_usage()
        elif t == 'ps':
            return self.ps(self)
        elif t == 'mem':
            return self.get_mem_usage()
        elif t == 'last':
            return self.last(self)
        elif t == 'df':
            return self.df(self)
        else:
            self.hello_world()
