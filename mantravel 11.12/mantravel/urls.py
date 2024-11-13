"""
URL configuration for mantravel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from trip.views import kimi_chat_view

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
# 定义一个简单的视图函数作为根路径
def home(request):
    return HttpResponse("Welcome to the homepage!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kimi-chat/', kimi_chat_view, name='kimi_chat'),
    path('api/accounts/', include('accounts.urls')),  # 包含 accounts 应用的路由
    path('', home),  # 根路径配置
    path('api/memos/', include('memo.urls')),  # 包含备忘录应用的路由
    path('api/bills/', include('bills.urls')),
]
