from .models import TranslateRecord
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.http import JsonResponse
from base.utils import *

def query(request):
    print(request)
    print(request.method)
    print(request.content_type)
    print(request.content_params)
    print(request.body)
    print(request.path_info)
    print(request.GET)
    words = request.GET['words']
    print(words)
    src_content = request.GET['src_content']
    display_content = request.GET['display_content']
    try:
        trs = TranslateRecord.objects.get(words_text=words)
        trs.quest_num += 1
        trs.last_quest_date = timezone.now()
        trs.save()
        return JsonResponse(Result(RESULT_SUCCESS, "成功创建").getJsonStr())
    except ObjectDoesNotExist:
        trs = TranslateRecord()
        trs.words_text = words
        trs.src_content = src_content
        trs.last_quest_date = timezone.now()
        trs.display_content = display_content
        trs.save()
        # queryset.values() --> dict
        return JsonResponse(Result(RESULT_SUCCESS, "成功更新").getJsonStr())


def delete(request):
    words = request.GET['words']
    TranslateRecord.objects.filter(words_text=words).update(is_deleted=True)
    return JsonResponse(Result(RESULT_SUCCESS, "删除成功").getJsonStr())


def rembered(request):
    words = request.GET['words']
    TranslateRecord.objects.filter(words_text=words).update(is_rembered=True)
    return JsonResponse(Result(RESULT_SUCCESS, "已成功记住").getJsonStr())


def deleted_list(request):
    record_list = TranslateRecord.objects.filter(is_deleted=True).values()
    return JsonResponse(Result(RESULT_SUCCESS, "查询成功").getJsonStr(getlist(record_list)))


def rembered_list(request):
    record_list = TranslateRecord.objects.filter(is_rembered=True).values()
    return JsonResponse(Result(RESULT_SUCCESS, "查询成功").getJsonStr(getlist(record_list)))


def list(request):
    page = request.GET.get('page')
    type =  int(request.GET.get('type'))


    print(type)
    if type == 0:
        record_list = TranslateRecord.objects.filter(is_deleted=False).order_by('-last_quest_date').values()
    elif type == 1:
        print(type)
        record_list = TranslateRecord.objects.filter(is_deleted=False).order_by('-quest_num').values()
    else:
        record_list = TranslateRecord.objects.filter(is_deleted=False).order_by('-last_quest_date').values()

    response = JsonResponse(page_infilter(record_list, page))
    return response


def remove(request):
    words = request.GET['words']
    TranslateRecord.objects.filter(words_text=words).delete()
    return JsonResponse(Result(RESULT_SUCCESS, "删除成功").getJsonStr())

#
#
# def delete(words):
#
#
#
# def remembered():
