import hashlib
import time

from User.models import User


def verify_user(phone, password):
    # 验证是否存在账号
    user = User.objects.filter(user_phone=phone).first()
    if user:
        # 验证登录
        query_res = User.objects.filter(user_phone=phone, user_passwd=password).first()
        if query_res:
            return True, query_res
        else:
            return False, None
    else:
        return False, None


def exist_user(phone) -> bool:
    if User.objects.filter(user_phone=phone).first():
        return True
    else:
        return False


def calculate_userId(phone):
    username_hash = hashlib.sha256(phone.encode()).hexdigest()
    timestamp = int(time.time())
    userId = str(timestamp) + username_hash[:5]

    return userId


def add_user(phone, password) -> bool:
    # 检测数据库是否存在
    if exist_user(phone):
        return False
    else:
        User.objects.create(
            user_id=calculate_userId(phone),
            user_name=phone,
            user_phone=phone,
            user_passwd=password
        )
        return True
