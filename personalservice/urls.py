"""personalservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from translaterservice import translate_records, user
from rest_framework.authtoken.views import obtain_auth_token
from translaterservice import sever_manger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    path('translate_record/list', translate_records.record_list),
    path('translate_record/query', translate_records.query),
    path('translate_record/delete', translate_records.delete),
    path('translate_record/remove', translate_records.remove),
    path('translate_record/deleted_list', translate_records.deleted_list),
    path('translate_record/remembered_list', translate_records.remembered_list),
    path('translate_record/remembered', translate_records.remembered),

    path('user/create_user_step1', user.create_user_step1),
    path('user/create_user_step2', user.create_user_step2),
    path('user/change_pwd_step1', user.change_pwd_step1),
    path('user/change_pwd_step2', user.change_pwd_step2),
    path('user/all', user.users),

    path('server/info', sever_manger.ServerView.as_view(), name='get')
]
