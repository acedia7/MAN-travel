# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)  # 使用手机号作为唯一标识
    username = None  # 移除用户名字段
    access_token = models.TextField(null=True, blank=True)  # 添加 access_token 字段

    USERNAME_FIELD = 'phone'  # 设置手机号为登录字段
    REQUIRED_FIELDS = []  # 不需要其他必填字段

    def __str__(self):
        return self.phone