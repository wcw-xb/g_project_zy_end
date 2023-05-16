import copy
import datetime

from django.shortcuts import render
from django.http import JsonResponse
from User.views import RETURN_DATA
from Util.TokenManage import authentication
from Home.models import SportsInfo


# Create your views here.
@authentication
def update_steps(request):
    if request.method == "GET":
        return_data = copy.deepcopy(RETURN_DATA)
        user_id = request.user.user_id
        sport = SportsInfo.objects.filter(user_id=user_id, now_time=datetime.date.today()).first()
        sport.steps = request.GET.get("steps")
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
