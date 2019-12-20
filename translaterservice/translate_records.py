import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone

from base.utils import *
from .models import TranslateRecord


def query(request):
    print(request)
    print("````````````")
    print(request.headers)
    print("````````````")
    data = json.loads(request.body)
    print(data)

    words = data['words']
    src_content = data['src']
    display_content = data['show_content']

    try:
        trs = TranslateRecord.objects.get(words_text=words)
        trs.quest_num += 1
        trs.last_quest_date = timezone.now()
        trs.save()
        return JsonResponse(Result(RESULT_SUCCESS, "成功创建").get_json_str())
    except ObjectDoesNotExist:
        trs = TranslateRecord()
        trs.words_text = words
        trs.src_content = src_content
        trs.last_quest_date = timezone.now()
        trs.display_content = display_content
        trs.save()
        # queryset.values() --> dict
        return JsonResponse(Result(RESULT_SUCCESS, "成功更新").get_json_str())


def delete(request):
    words = request.GET['words']
    TranslateRecord.objects.filter(words_text=words).update(is_deleted=True)
    return JsonResponse(Result(RESULT_SUCCESS, "删除成功").get_json_str())


def remembered(request):
    words = request.GET['words']
    TranslateRecord.objects.filter(words_text=words).update(is_rembered=True)
    return JsonResponse(Result(RESULT_SUCCESS, "已成功记住").get_json_str())


def deleted_list(request):
    lists = TranslateRecord.objects.filter(is_deleted=True).values()
    return JsonResponse(Result(RESULT_SUCCESS, "查询成功").get_json_str(getlist(lists)))


def remembered_list(request):
    lists = TranslateRecord.objects.filter(is_rembered=True).values()
    return JsonResponse(Result(RESULT_SUCCESS, "查询成功").get_json_str(getlist(lists)))


def record_list(request):
    page = request.GET.get('page')
    t = int(request.GET.get('type'))

    print(t)
    if t == 0:
        lists = TranslateRecord.objects.filter(is_deleted=False).order_by('-last_quest_date').values()
    elif t == 1:
        print(t)
        lists = TranslateRecord.objects.filter(is_deleted=False).order_by('-quest_num').values()
    else:
        lists = TranslateRecord.objects.filter(is_deleted=False).order_by('-last_quest_date').values()

    response = JsonResponse(get_page(lists, page))
    return response


def remove(request):
    words = request.GET['words']
    TranslateRecord.objects.filter(words_text=words).delete()
    return JsonResponse(Result(RESULT_SUCCESS, "删除成功").get_json_str())

#
#
# def delete(words):
#
#
#
# def remembered():
