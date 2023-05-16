import copy

from django.http import JsonResponse
from django.views import View
from django.core.handlers.wsgi import WSGIRequest

from Util.TokenManage import generate_token
from Util.UserManage import verify_user, add_user

RETURN_DATA = {
    "status": 1,
    "error": "",
    "content": ""
}


class Login(View):
    def get(self, request: WSGIRequest):
        return_data = copy.deepcopy(RETURN_DATA)
        user_phone = request.GET.get("phone", None)
        password = request.GET.get("passwd", None)
        if not user_phone or not password:
            return_data["error"] = "账号和用户名不能为空"
            return JsonResponse(return_data)
        user_correctness, user = verify_user(user_phone, password)  # 判断是否存在user
        if user_correctness:
            return_data["content"] = "登录成功"
            # 生成jwt的token
            return_data["token"] = generate_token(user)
            return_data["data"] = {
                "uname": user.user_name,
                "height": user.height,
                "weight": user.weight,
                "age": user.age
            }
        else:
            return_data["status"] = 0
            return_data["error"] = "账号密码错误"
        return JsonResponse(return_data)


class Register(View):
    """
    注册
    """

    def get(self, request: WSGIRequest):
        return_data = copy.deepcopy(RETURN_DATA)
        user_phone = request.GET.get("phone", None)
        password = request.GET.get("passwd", None)
        if user_phone and password:
            register_res = add_user(user_phone, password)
            if register_res:  # 添加成功
                return_data["content"] = "注册成功"
            else:  # 添加失败
                return_data["status"] = 0
                return_data["error"] = "注册失败"
        else:
            return_data["status"] = 0
            return_data["error"] = "账号密码不能为空"
        return JsonResponse(return_data)
