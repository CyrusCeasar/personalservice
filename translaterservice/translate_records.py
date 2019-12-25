import json
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone

from base.bean.models import RESULT_FAILED
from base.http_headers import *
from translaterservice.models import *

from base.utils import *


def lookup(request):
    data = json.loads(request.body)

    print(data)

    word = data.get('word')
    src_content = data.get('src_content')
    display_content = data.get('display_content')

    device_id = request.headers.get(DEVICE_ID)
    user_id = request.headers.get(USER_ID)
    print(request.headers)
    if src_content and display_content and word and device_id:

        vocabulary, created = Vocabulary.objects.filter(word=word).get_or_create(word=word, src_content=src_content,
                                                                                 display_content=display_content)
        if user_id:
            trs, created = LookUpRecord.objects.filter(vocabulary_id=word, user_id=user_id).get_or_create(
                vocabulary=vocabulary)
        else:
            trs, created = LookUpRecord.objects.filter(vocabulary_id=word, device_id=device_id,
                                                       user_id__isnull=True).get_or_create(vocabulary=vocabulary)
        trs.user_id = user_id
        trs.device_id = device_id
        trs.lookup_amount = trs.lookup_amount + 1
        trs.last_lookup_time = timezone.now()
        trs.save()
        return JsonResponse(Result(RESULT_SUCCESS, "查找成功").get_json_str())
    else:
        return JsonResponse(Result(RESULT_FAILED, "缺少必要参数").get_json_str())


def synchronise_translate_records(device_id, user_id):
    LookUpRecord.objects.filter(user_id__isnull=True, device_id=device_id).update(user_id=user_id)


def delete(request):
    data = json.loads(request.body)
    device_id = request.headers.get(DEVICE_ID)
    user_id = request.headers.get(USER_ID)
    word = data.get('word')
    if user_id:
        LookUpRecord.objects.filter(vocabulary_id=word, user_id=user_id).update(deleted=True)
    else:
        LookUpRecord.objects.filter(vocabulary_id=word, user_id__isnull=True, device_id=device_id).update(deleted=True)
    return JsonResponse(Result(RESULT_SUCCESS, "删除成功").get_json_str())


def remembered(request):
    data = json.loads(request.body)
    device_id = request.headers.get(DEVICE_ID)
    user_id = request.headers.get(USER_ID)
    word = data.get('word')
    if user_id:
        LookUpRecord.objects.filter(vocabulary_id=word, user_id=user_id).update(remembered=True)
    else:
        LookUpRecord.objects.filter(vocabulary_id=word, user_id__isnull=True, device_id=device_id).update(
            remembered=True)

    return JsonResponse(Result(RESULT_SUCCESS, "删除成功").get_json_str())


def deleted_list(request):
    device_id = request.headers.get(DEVICE_ID)
    user_id = request.headers.get(USER_ID)
    if user_id:
        lists = LookUpRecord.objects.filter(deleted=True, user_id=user_id).values()
        return JsonResponse(Result(RESULT_SUCCESS, "查询成功").get_json_str(getlist(lists)))
    else:
        lists = LookUpRecord.objects.filter(deleted=True, device_id=device_id, user_id__isnull=True).values()
        return JsonResponse(Result(RESULT_SUCCESS, "查询成功").get_json_str(getlist(lists)))


def remembered_list(request):
    device_id = request.headers.get(DEVICE_ID)
    user_id = request.headers.get(USER_ID)
    if user_id:
        lists = LookUpRecord.objects.filter(remembered=True, user_id=user_id).values()
        return JsonResponse(Result(RESULT_SUCCESS, "查询成功").get_json_str(getlist(lists)))
    else:
        lists = LookUpRecord.objects.filter(remembered=True, device_id=device_id, user_id__isnull=True).values()
        return JsonResponse(Result(RESULT_SUCCESS, "查询成功").get_json_str(getlist(lists)))


def record_list(request):
    page = request.GET.get('page')
    t = int(request.GET.get('type'))

    device_id = request.headers.get(DEVICE_ID)
    user_id = request.headers.get(USER_ID)

    order_by = '-lookup_amount' if t == 1 else '-last_lookup_time'

    if user_id:
        qst = LookUpRecord.objects.filter(deleted=False, user_id=user_id).order_by(order_by)
    else:
        qst = LookUpRecord.objects.filter(deleted=False, device_id=device_id, user_id__isnull=True).order_by(order_by)

    lists = qst.values('id', 'lookup_amount', 'last_lookup_time',
                       'vocabulary__src_content', 'vocabulary__display_content',
                       'vocabulary__word')
    response = JsonResponse(get_page(lists, page))
    return response


def remove(request):
    data = json.loads(request.body)
    device_id = request.headers.get(DEVICE_ID)
    user_id = request.headers.get(USER_ID)
    word = data.get('word')
    if user_id:
        LookUpRecord.objects.filter(vocabulary_id=word, user_id=user_id).delete()
    else:
        LookUpRecord.objects.filter(vocabulary_id=word, user_id__isnull=True, device_id=device_id).delete()
    return JsonResponse(Result(RESULT_SUCCESS, "删除成功").get_json_str())

#
#
# def delete(words):
#
#
#
# def remembered():
