import json

import pyotp
from django.contrib.auth import authenticate
from django.core import serializers
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
import time

from base.bean.models import RESULT_FAILED
from base.tokens import TokenGenerator
from base.utils import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.core.cache import cache
from base import verifyUtils
from base import mailutils


def hello(request):
    cache.set("foo", "foo", timeout=25)
    return JsonResponse(Result(RESULT_SUCCESS, cache.get("foo")).getJsonStr())


def createUserStep1(request):
    email = request.GET['email']
    if verifyUtils.isEmail(email):
        authentication_code = cache.get(email)
        if authentication_code:
            mailutils.send_mail(email, "AuthCode", authentication_code)
        else:
            hotp = pyotp.HOTP('base32secret3232')
            authentication_code = hotp.at(int(time.time() * 1000))
            mailutils.send_mail(email, "AuthCode" + time.time().__str__(), authentication_code)
            cache.set(email, authentication_code, timeout=60 * 5)
        return JsonResponse(Result(RESULT_SUCCESS, "验证码发送成功").getJsonStr())
    else:
        return JsonResponse(Result(RESULT_FAILED, "邮箱格式不符合").getJsonStr())


def createUserStep2(request):
    datas = json.loads(request.body)
    authcode = datas['auth_code']
    email = datas["email"]
    pwd = datas["pwd"]
    print(str(authcode), cache.get(email))
    if str(authcode) == cache.get(email):
        user = User.objects.create_user(email, email, pwd)
        user.save()
        tmpJson = serializers.serialize("json", user)
        tmpObj = json.loads(tmpJson)
        return JsonResponse(Result(RESULT_SUCCESS, "创建成功").getJsonStr(tmpObj))
    else:
        return JsonResponse(Result(RESULT_FAILED, "验证码已过期").getJsonStr())


def users(request):
    record_list = User.objects.all()
    tmpJson = serializers.serialize("json", record_list)
    tmpObj = json.loads(tmpJson)
    return JsonResponse(Result(RESULT_SUCCESS, "查询成功").getJsonStr(tmpObj))


