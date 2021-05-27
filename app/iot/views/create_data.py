from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

from .models import IotModel

import secrets
import datetime



def dict_to_list(dic):
    lst = []
    for e in dic.items():
        lst.extend(e)
    return lst


def datafunc(request, **kwargs):
    hiro_id = getattr(settings, 'PROJECT_ID')
    content = kwargs.get('contents')
    key = content[0:len(hiro_id)]
    if secrets.compare_digest(key, hiro_id):
        alluser_last_name = [i for i in User.objects.values('last_name')]
        alluser_last_name_values =[dict_to_list(i)[1] for i in alluser_last_name if dict_to_list(i)[1] != '']
        list = content.split(',')
        TF = [list[0] == i for i in alluser_last_name_values]
        if sum(TF) != 1:
            return HttpResponseBadRequest()
        else:
            content_position = len(list[0]) + len(list[1]) + 2
            dt_now = datetime.datetime.now()
            now_ts = int(dt_now.timestamp())
            model = IotModel.objects.create(token=list[0], device=list[1], time=str(now_ts), content=content[content_position:])
            return HttpResponse(now_ts)
    else:
        return HttpResponseBadRequest()