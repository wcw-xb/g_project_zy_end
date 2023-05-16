from django.db import models


# Create your models here.
class MonitorData(models.Model):
    user_id = models.IntegerField()  # 用户id
    monitor_time = models.DateTimeField()  # 监测时间
    monitor_star = models.IntegerField()  # 监测星级
    status = models.CharField(max_length=20)  # 监测状态
