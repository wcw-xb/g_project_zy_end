from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
class SportsInfo(models.Model):
    user_id = models.IntegerField()  # 用户id
    now_time = models.DateTimeField(validators=[
        RegexValidator(
            regex=r'^\d{4}-\d{2}-\d{2}$',
            message='Invalid datetime format. Please use the format "YYYY-MM-DD".'
        )
    ])
    sports_time = models.IntegerField()  # 运动时间
    steps = models.IntegerField()  # 步数
    heat = models.IntegerField()  # 热量


class WalkData(models.Model):
    user_id = models.IntegerField()  # 用户id
    now_time = models.DateTimeField(validators=[
        RegexValidator(
            regex=r'^\d{4}-\d{2}-\d{2}$',
            message='Invalid datetime format. Please use the format "YYYY-MM-DD".'
        )
    ])
    walk_rate = models.FloatField()  # 用户的行走速度
    walk_time = models.IntegerField()  # 用户的行走时长


class SitData(models.Model):
    user_id = models.IntegerField()  # 用户id
    now_time = models.DateTimeField(validators=[
        RegexValidator(
            regex=r'^\d{4}-\d{2}-\d{2}$',
            message='Invalid datetime format. Please use the format "YYYY-MM-DD".'
        )
    ])
    sit_time = models.IntegerField()  # 用户的坐立时长


class RunData(models.Model):
    user_id = models.IntegerField()  # 用户id
    now_time = models.DateTimeField(validators=[
        RegexValidator(
            regex=r'^\d{4}-\d{2}-\d{2}$',
            message='Invalid datetime format. Please use the format "YYYY-MM-DD".'
        )
    ])
    run_rate = models.FloatField()  # 用户的跑步速度
    run_time = models.IntegerField()  # 用户的跑步时长


class LatestStatus(models.Model):
    # 记录最新的用户状态
    user_id = models.IntegerField()  # 用户id
    status = models.CharField(max_length=10, default="暂无")
    data = models.FloatField()  # 状态数据
