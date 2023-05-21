import copy
import datetime
import json
import pickle

import numpy as np
from django.core.cache import cache
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from User.views import RETURN_DATA
from Util.TokenManage import authentication
from Home.models import SportsInfo, WalkData, RunData, SitData, CollisionInfo
import pandas as pd

Status = {
    "1": "坐姿",
    "2": "走路",
    "3": "跑步",
}


@authentication
def update_steps(request):
    if request.method == "GET":
        return_data = copy.deepcopy(RETURN_DATA)
        user_id = request.user.user_id
        sport = SportsInfo.objects.filter(user_id=user_id, now_time=datetime.date.today()).first()
        if not sport:
            # 没有数据
            SportsInfo.objects.create(
                user_id=user_id,
                now_time=datetime.date.today(),
                sports_time=0,
                steps=request.GET.get("step"),
                heat=int(int(request.GET.get("step")) * int(request.user.height) * 0.000693)
            )
        else:
            sport.steps = request.GET.get("step")
            sport.save()
        return_data["content"] = "success"
        return JsonResponse(return_data)


@authentication
def get_steps(request):
    if request.method == "GET":
        return_data = copy.deepcopy(RETURN_DATA)
        user_id = request.user.user_id
        sport = SportsInfo.objects.filter(user_id=user_id, now_time=datetime.date.today()).first()
        return_data["data"] = sport.steps
        return JsonResponse(return_data)


def record_latest_status(status_li, user_id):
    """
    记录最新状态
    """
    tag = f"{status_li.index(max(status_li)) + 1}"
    tag_res = Status[tag]
    if tag_res == '走路':
        data = f"{round(WalkData.objects.filter(user_id=user_id, now_time=datetime.date.today()).first().walk_rate, 2)} m/s"
    elif tag_res == "坐姿":
        data = f"{SitData.objects.filter(user_id=user_id, now_time=datetime.date.today()).first().sit_time} s(秒)"
    else:
        data = f"{round(RunData.objects.filter(user_id=user_id, now_time=datetime.date.today()).first().run_rate, 2)} m/s"
    return str(tag_res), str(data)


def collision_monitor(predicted_targets, data, user_id):
    magnitudes = [np.linalg.norm(reading) for reading in data]
    # 计算加加速度
    jerk = np.diff(magnitudes)
    # 划分碰撞强度的阈值，根据实际情况调整
    thresholds = [5, 10, 20, 30]
    # 以此类推
    levels = list(np.digitize(jerk, thresholds))
    if max(levels) >= 2:
        CollisionInfo.objects.create(
            user_id=user_id,
            collision_day=datetime.datetime.now().date(),
            collision_time=datetime.datetime.now().time(),
            level=max(levels) + 1
        )
    if 3 in levels or 4 in levels:
        # 碰撞严重
        return True
    return False


@authentication
def upload_sensor_data(request):
    return_data = copy.deepcopy(RETURN_DATA)
    if request.method == "POST":
        request_data = json.loads(request.body.decode())
        if not request_data["data"]:
            return JsonResponse(return_data)
        model_from_cache = cache.get("random_forest_model")
        if model_from_cache is None:
            from Home.load_model import load_model
            model = load_model()
            cache.set("random_forest_model", pickle.dumps(model))
        else:
            model = pickle.loads(model_from_cache)
        data = pd.DataFrame(request_data["data"], columns=['x_data', 'y_data', 'z_data'])
        duration = request_data["duration"]
        predicted_targets = [int(x) for x in list(model.predict(data))]
        # 碰撞监测
        collision_res = collision_monitor(predicted_targets, request_data["data"], request.user.user_id)
        sit_time = round(predicted_targets.count(1) * duration / len(predicted_targets))  # 坐姿
        # stand_time = round(predicted_targets.count(2) * duration / len(predicted_targets), 2)  # 站姿
        # sleep_time = round(predicted_targets.count(3) * duration / len(predicted_targets), 2)  # 卧姿
        walk_time = round(predicted_targets.count(4) * duration / len(predicted_targets), 2)  # 走路
        run_time = round(predicted_targets.count(5) * duration / len(predicted_targets), 2)  # 跑步
        # go_up_time = round(predicted_targets.count(6) * duration / len(predicted_targets), 2)  # 上楼
        # go_down_time = round(predicted_targets.count(7) * duration / len(predicted_targets), 2)  # 下楼
        status_li = [sit_time, walk_time, run_time]
        sports_time = status_li[2]
        sport = SportsInfo.objects.filter(user_id=request.user.user_id, now_time=datetime.date.today()).first()
        if not sport:
            sport = SportsInfo.objects.create(user_id=request.user.user_id, now_time=datetime.date.today())
        if sport.sports_time:
            sport.sports_time += sports_time
        else:
            sport.sports_time = sports_time

        sport.save()
        # 行走数据
        walk = WalkData.objects.filter(user_id=request.user.user_id, now_time=datetime.date.today()).first()
        if not walk:
            walk = WalkData.objects.create(user_id=request.user.user_id, now_time=datetime.date.today(), walk_rate=0,
                                           walk_time=0)
        if walk.walk_time:
            walk.walk_time += status_li[1]
        else:
            walk.walk_time = status_li[1]
        if Status[f"{status_li.index(max(status_li)) + 1}"] == "走路":
            accelerations = np.array(request_data["data"])
            delta_t = duration / len(predicted_targets)
            velocities = np.cumsum(accelerations * delta_t, axis=0)
            abs_velocities = np.abs(velocities)  # 取速度的绝对值
            walk_rate = np.mean(np.mean(abs_velocities, axis=0))
            walk.walk_rate = walk_rate
            walk.walk_clock = datetime.datetime.now().time()
        walk.save()
        # 跑步数据
        run = RunData.objects.filter(user_id=request.user.user_id, now_time=datetime.date.today()).first()
        if not run:
            run = RunData.objects.create(user_id=request.user.user_id, now_time=datetime.date.today(), run_rate=0,
                                         run_time=0)
        if run.run_time:
            run.run_time += status_li[2]
        else:
            run.run_time = status_li[2]
        if Status[f"{status_li.index(max(status_li)) + 1}"] == "跑步":
            accelerations = np.array(request_data["data"])
            delta_t = duration / len(predicted_targets)
            velocities = np.cumsum(accelerations * delta_t, axis=0)
            abs_velocities = np.abs(velocities)  # 取速度的绝对值
            run_rate = np.mean(np.mean(abs_velocities, axis=0))
            run.run_rate = run_rate
            run.run_clock = datetime.datetime.now().time()
        run.save()
        # 坐立数据
        sit = SitData.objects.filter(user_id=request.user.user_id, now_time=datetime.date.today()).first()
        if not sit:
            sit = SitData.objects.create(user_id=request.user.user_id, now_time=datetime.date.today(), sit_time=0)
        if sit.sit_time:
            sit.sit_time += status_li[0]
        else:
            sit.sit_time += status_li[0]
        if Status[f"{status_li.index(max(status_li)) + 1}"] == "坐姿":
            sit.sit_clock = datetime.datetime.now().time()
        sit.save()
        status, data = record_latest_status(status_li, request.user.user_id)
        return_data["latest"] = {
            "status": status,
            "value": data
        }
        return_data["data"] = status_li
        return_data["info"] = {
            "status": Status[f"{status_li.index(max(status_li)) + 1}"],
            "sports_time": sport.sports_time,
            "walk_info": {
                "walk_time": walk.walk_time,
                "walk_rate": walk.walk_rate,
                "walk_clock": walk.walk_clock
            },
            "run_info": {
                "run_time": run.run_time,
                "run_rate": run.run_rate,
                "run_clock": run.run_clock
            },
            "sit_info": {
                "sit_time": sit.sit_time,
                "sit_clock": sit.sit_clock
            },
            "collision": collision_res
        }
    print("collision&&&", collision_res)
    return JsonResponse(return_data)


@authentication
def show_data(request):
    if request.method == "GET":
        return_data = copy.deepcopy(RETURN_DATA)
        sport = SportsInfo.objects.filter(user_id=request.user.user_id, now_time=datetime.date.today()).first()
        walk = WalkData.objects.filter(user_id=request.user.user_id, now_time=datetime.date.today()).first()
        run = RunData.objects.filter(user_id=request.user.user_id, now_time=datetime.date.today()).first()
        sit = SitData.objects.filter(user_id=request.user.user_id, now_time=datetime.date.today()).first()
        return_data["info"] = {
            "sports_time": sport.sports_time,
            "walk_info": {
                "walk_time": walk.walk_time,
                "walk_rate": walk.walk_rate,
                "walk_clock": walk.walk_clock
            },
            "run_info": {
                "run_time": run.run_time,
                "run_rate": run.run_rate,
                "run_clock": run.run_clock
            },
            "sit_info": {
                "sit_time": sit.sit_time,
                "sit_clock": sit.sit_clock
            }
        }
        return JsonResponse(return_data)


def collision_sort_key(collision_data):
    d_time = datetime.datetime.strptime(collision_data["collision_day"], "%Y-%m-%d")
    return d_time


@authentication
def monitor_data(request):
    if request.method == "GET":
        collision_obj = CollisionInfo.objects.filter(user_id=request.user.user_id).all()
        all_data = []
        for collision in collision_obj:
            data = {
                "collision_day": collision.collision_day.strftime("%Y-%m-%d"),
                "collision_time": collision.collision_time.strftime("%H:%M:%S"),
                "level": collision.level
            }
            all_data.append(data)
        return HttpResponse(json.dumps(sorted(all_data, key=collision_sort_key, reverse=True)))
