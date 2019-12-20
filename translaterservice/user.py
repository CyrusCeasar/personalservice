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


def send_authentication_code(email):
    hotp = pyotp.HOTP('base32secret3232')
    authentication_code = hotp.at(int(time.time() * 1000))
    mailutils.send_mail(email, "AuthCode" + time.time().__str__(), authentication_code)
    cache.set(email, authentication_code, timeout=60 * 5)


def create_user_step1(request):
    email = request.GET['email']
    if verifyUtils.isEmail(email):
        authentication_code = cache.get(email)
        if authentication_code:
            mailutils.send_mail(email, "AuthCode", authentication_code)
        else:
            send_authentication_code(email)
        return JsonResponse(Result(RESULT_SUCCESS, "验证码发送成功").get_json_str())
    else:
        return JsonResponse(Result(RESULT_FAILED, "邮箱格式不符合").get_json_str())


def create_user_step2(request):
    data = json.loads(request.body)
    auth_code = data['auth_code']
    email = data["email"]
    pwd = data["pwd"]
    print(str(auth_code), cache.get(email))
    if str(auth_code) == cache.get(email):
        user = User.objects.create_user(email, email, pwd)
        user.save()
        tmp_json = serializers.serialize("json", user)
        tmp_obj = json.loads(tmp_json)
        return JsonResponse(Result(RESULT_SUCCESS, "创建成功").get_json_str(tmp_obj))
    else:
        return JsonResponse(Result(RESULT_FAILED, "验证码已过期").get_json_str())


def users(request):
    record_list = User.objects.all()
    tmp_json = serializers.serialize("json", record_list)
    tmp_obj = json.loads(tmp_json)
    return JsonResponse(Result(RESULT_SUCCESS, "查询成功").get_json_str(tmp_obj))


def change_pwd_step1(request):
    email = request.POST['email']
    obj, created = User.objects.filter(email=email).get_or_create()
    if created:
        return JsonResponse(Result(RESULT_FAILED, "用户不存在").get_json_str())
    else:
        send_authentication_code(email)
        return JsonResponse(Result(RESULT_SUCCESS, "验证码发送成功").get_json_str())


def change_pwd_step2(request):
    email = request.POST['email']
    pwd = request.POST['password']
    auth_code = cache.get(email)
    if auth_code:
        obj, created = User.objects.filter(email=email).get_or_create()
        if created:
            return JsonResponse(Result(RESULT_FAILED, "用户不存在").get_json_str())
        else:
            obj.password = pwd
            obj.save()
            return JsonResponse(Result(RESULT_SUCCESS, "密码修改成功").get_json_str())
    else:
        return JsonResponse(Result(RESULT_FAILED, "验证码已过期").get_json_str())
