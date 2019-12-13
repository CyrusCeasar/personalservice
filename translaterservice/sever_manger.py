import subprocess
from django.http import JsonResponse
from base.utils import *
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


def getMemUsage(request):
    return JsonResponse(Result(RESULT_SUCCESS, "成功获取").getJsonStr(getVpsCacheUsage()))


def getCpuUsuage(request):
    result = subprocess.run(['mpstat'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
    return JsonResponse(Result(RESULT_SUCCESS, "成功获取").getJsonStr(result))


def ps(request):
    result = subprocess.run(['ps', '-ejf'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
    return JsonResponse(Result(RESULT_SUCCESS, "成功获取").getJsonStr(result))


def last(request):
    result = os.popen('last | grep "logged in"').read().splitlines()
    return JsonResponse(Result(RESULT_SUCCESS, "成功获取").getJsonStr(result))


def df(request):
    result = subprocess.run(['df', '-h'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
    return JsonResponse(Result(RESULT_SUCCESS, "成功获取").getJsonStr(result))


def getVpsCacheUsage():
    result = subprocess.run(['free', '-h'], stdout=subprocess.PIPE).stdout.decode(UTF_8).splitlines()
    return result
