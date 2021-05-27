from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import IotModel

import datetime

from django_pandas.io import read_frame


@login_required
def dlfunc(request):
    try:
        username = request.user.get_username()
        t =User.objects.filter(username__contains=username).values('last_name')
        user_db = IotModel.objects.filter(token__contains=t)
        df = read_frame(user_db, fieldnames=['device', 'time', 'content'])
        now_ts = int(datetime.datetime.now().timestamp())
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=['+ str(now_ts) +']mypage.csv'
        df.to_csv(path_or_buf=response,index=False)
        return response
    except:
        return redirect('login')


@login_required
def deletefunc(request):
    try:
        username = request.user.get_username()
        t =User.objects.filter(username__contains=username).values('last_name')
        user_db = IotModel.objects.filter(token__contains=t)
        user_db.delete()
        return redirect('read')
    except:
        return redirect('login')