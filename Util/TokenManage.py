import copy
from datetime import datetime, timedelta
import jwt
import django.conf
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from User.models import User

RETURN_DATA = {
    "status": 1,
    "error": "",
    "content": ""
}


def generate_token(user):
    secret_key = django.conf.settings.SECRET_KEY
    payload = {
        "user_id": user.user_id,
        "user_phone": user.user_phone,
        "exp": datetime.utcnow() + timedelta(days=30)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def getUserFromToken(token):
    try:
        payload = jwt.decode(token.encode(), django.conf.settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        user_phone = payload["user_phone"]
        user = User.objects.filter(user_id=user_id, user_phone=user_phone).first()
        return user
    except jwt.ExpiredSignatureError:
        return JsonResponse({"status": 0, "content": "token已过期, 请重新登录"})
    except jwt.InvalidTokenError:
        return JsonResponse({"status": 0, "content": "无效的token, 请重新登录"})


def authentication(function):
    def inner(request: WSGIRequest, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION", None)
        if token and len(token.split(" ")) == 2:
            token = token.split(" ")[1]
            user = getUserFromToken(token)
            if isinstance(user, JsonResponse):
                return user
            else:
                request.user = user
        else:
            data = copy.deepcopy(RETURN_DATA)
            data["status"] = 0
            data["error"] = "缺少token，请登录后访问"
            return JsonResponse(data)
        return function(request, *args, **kwargs)

    return inner
