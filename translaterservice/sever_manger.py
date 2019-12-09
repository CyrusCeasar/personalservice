import subprocess
from django.http import JsonResponse
from base.utils import *

class MemUsage:
    name = "mem"
    total = ""
    used = ""
    free = ""
    shared = ""
    cache = ""
    available = ""

def getMemUsage(request):
    return JsonResponse(Result(RESULT_SUCCESS,"成功获取").getJsonStr(getVpsCacheUsage()))


def getCpuUsuage(request):
    result = subprocess.run(['mpstat'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()
    return JsonResponse(Result(RESULT_SUCCESS, "成功获取").getJsonStr(result))


def getVpsCacheUsage():
    result = subprocess.run(['free', '-h'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return  result


