from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from base.bean.models import Result, RESULT_SUCCESS


def getlist(obj):
    return None if len(obj) == 0 else list(obj)


def get_page(obj, page, pagesize=20):
    paginator = Paginator(obj, pagesize)
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        result_list = list()
    return Result(RESULT_SUCCESS, "查询成功").get_json_str(getlist(result_list))

