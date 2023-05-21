"""gra_project_zy_end URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from User.views import Login, Register, update_username, update_height, update_weight, update_age
from Home.views import update_steps, get_steps, upload_sensor_data, show_data, monitor_data

urlpatterns = [
    # 用户
    path("login/", Login.as_view()),
    path("register/", Register.as_view()),
    path("update_username", update_username),
    path("update_height", update_height),
    path("update_weight", update_weight),
    path("update_age", update_age),

    # 首页
    path("update_steps", update_steps),
    path("get_steps", get_steps),
    path("upload_sensor_data", upload_sensor_data),
    path("show_data", show_data),
    path("monitor_data", monitor_data),


]
