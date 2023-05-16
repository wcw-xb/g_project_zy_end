from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=50, null=False)
    user_name = models.CharField(max_length=20, null=False)
    user_passwd = models.CharField(max_length=20, null=False, default=None)
    user_phone = models.CharField(max_length=11, null=False, default=None)
    register_time = models.DateTimeField(auto_now_add=True)  # 设置用户注册的时间
    height = models.IntegerField(null=True, blank=True, default=0)  # 身高
    weight = models.IntegerField(null=True, blank=True, default=0)  # 体重
    age = models.IntegerField(null=True, blank=True, default=0)  # 年龄
