import datetime

from Home.models import SportsInfo


def get_steps(user_id):
    sports = SportsInfo.objects.filter(user_id=user_id, now_time=datetime.date.today()).first()
    if sports:
        return sports.steps
    else:
        return 0
