from django.db import models
from django.conf import settings  # 导入 settings

class Memo(models.Model):
    STATUS_CHOICES = [
        ('yes', '带了行李'),
        ('no', '没带行李'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 更新为指向自定义用户模型
    name = models.CharField(max_length=100)  # 备忘录名称
    note = models.TextField()  # 备注
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)  # 状态
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间

    def __str__(self):
        return self.name