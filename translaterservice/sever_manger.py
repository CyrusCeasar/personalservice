import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from base.utils import *
from rest_framework.permissions import IsAuthenticated
import os


class MemUsage:
    name = "mem"
    total = ""
    used = ""
    free = ""
    shared = ""
    cache = ""
    available = ""


UTF_8 = 'utf-8'


def getVpsCacheUsage():
    result = subprocess.run(['free', '-h'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
    return result


class ServerView(APIView):
    permission_classes = (IsAuthenticated,)

    def helloWorld(self):
        return Response(Result(RESULT_SUCCESS, "成功获取").getJsonStr())

    def getMemUsage(self):
        return Response(Result(RESULT_SUCCESS, "成功获取").getJsonStr(getVpsCacheUsage()))

    def getCpuUsuage(self):
        result = subprocess.run(['mpstat'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
        return Response(Result(RESULT_SUCCESS, "成功获取").getJsonStr(result))

    def ps(self):
        result = subprocess.run(['ps', '-ejf'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
        return Response(Result(RESULT_SUCCESS, "成功获取").getJsonStr(result))

    def last(self):
        result = os.popen('last | grep "logged in"').read().splitlines()
        return Response(Result(RESULT_SUCCESS, "成功获取").getJsonStr(result))

    def df(self):
        result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
        return Response(Result(RESULT_SUCCESS, "成功获取").getJsonStr(result))

    def get(self,request):
        type = request.GET.get('type')
        if type == 'cpu':
           return self.getCpuUsuage()
        elif type == 'ps':
            return self.ps()
        elif type== 'mem':
            return  self.getMemUsage()
        elif type== 'last':
            return  self.last()
        elif type=='df':
            return self.df()
        else:
            self.helloWorld()



