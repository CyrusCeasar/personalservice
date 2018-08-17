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
from django.urls import path
from translaterservice import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('translate_record/list', views.list),
    path('translate_record/query', views.query),
    path('translate_record/delete', views.delete),
    path('translate_record/remove', views.remove),
    path('translate_record/deleted_list', views.deleted_list),
    path('translate_record/remebered_list', views.rembered_list),
    path('translate_record/rembered', views.rembered)
]