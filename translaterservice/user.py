import json
import time
import pyotp

from django.core import serializers
from django.http import JsonResponse

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from base.bean.models import RESULT_FAILED
from base.utils import *
from base import verifyUtils
from base import mailutils
from django.contrib.auth.models import User
from django.core.cache import cache

CACHE_TYPE_REGISTER = 1
CACHE_TYPE_CHANGE_PWD = 2


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)

        return Response(
            Result(RESULT_SUCCESS, "登录成功").get_json_str(
                {'token': token.key, 'username': user.username, 'uid': user.id}))


def send_authentication_code(email, type):
    hotp = pyotp.HOTP('base32secret3232')
    authentication_code = hotp.at(int(time.time() * 1000))
    mailutils.send_mail(email, "AuthCode" + time.time().__str__(), authentication_code)
    cache.set(email, authentication_code, itemtype=type, timeout=60 * 5)


def create_user_step1(request):
    email = request.GET['email']
    if verifyUtils.isEmail(email):
        authentication_code = cache.get(email, CACHE_TYPE_REGISTER)
        if authentication_code:
            mailutils.send_mail(email, "AuthCode", authentication_code)
        else:
            send_authentication_code(email, CACHE_TYPE_REGISTER)
        return JsonResponse(Result(RESULT_SUCCESS, "验证码发送成功").get_json_str())
    else:
        return JsonResponse(Result(RESULT_FAILED, "邮箱格式不符合").get_json_str())


def create_user_step2(request):
    data = json.loads(request.body)
    auth_code = data['auth_code']
    email = data["email"]
    pwd = data["pwd"]
    cache_auth_code = cache.get(email, itemtype=CACHE_TYPE_REGISTER)
    print(str(auth_code), cache_auth_code)
    if str(auth_code) == cache_auth_code:
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
        send_authentication_code(email, CACHE_TYPE_CHANGE_PWD)
        return JsonResponse(Result(RESULT_SUCCESS, "验证码发送成功").get_json_str())


def change_pwd_step2(request):
    email = request.POST['email']
    pwd = request.POST['password']
    auth_code = cache.get(email, itemtype=CACHE_TYPE_CHANGE_PWD)
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
