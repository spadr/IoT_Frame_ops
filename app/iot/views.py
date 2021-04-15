from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse,Http404, HttpResponseBadRequest

from .models import IotModel

import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np
import pandas as pd
import csv
import secrets
import datetime
from django_pandas.io import read_frame


def dict_to_list(dic):
    lst = []
    for e in dic.items():
        lst.extend(e)
    return lst


def memefunc(request):
    return render(request, 'top.html')


def signupfunc(request):
    if request.method == "POST":
        email = request.POST['emailadress']
        psw = request.POST['password']
        name = email.split('@')
        try :
            user = User.objects.create_user(name[0], email, psw)
            hash = getattr(settings, 'PROJECT_ID', ' ') + secrets.token_hex()
            user.is_active = False
            user.last_name = hash
            user.save()
            from_email = 'EMAIL_ADDRESS'
            recipient_list = [email]
            subject = 'Activate Your Account'
            current_site = get_current_site(request)
            domain = current_site.domain
            context = render_to_string('account_activation_email.html',{
                'protocol': request.scheme,
                'domain': domain,
                'token': dumps(user.pk),
                'user': user,
                'hash': hash,
            })
            send_mail(subject, context, from_email, recipient_list)
            return render(request, 'signup.html', {'error' : '登録したメールアドレスへ認証メールを送信しました。URLをクリックして、アカウントを有効化してください。' , 'error2':'Please confirm your email address to complete the registration'})
        except IntegrityError:
            return render(request, 'signup.html', {'error' : 'このユーザーはすでに登録されています。'})
    return render(request, 'signup.html')


def loginfunc(request):
    if request.method == "POST":
        email = request.POST['emailadress']
        psw = request.POST['password']
        name = email.split('@')
        username = name[0]
        user = authenticate(request, username=username, password=psw)
        if user is not None:
            login(request, user)
            return redirect('read')
        else:
            return render(request, 'login.html', {'context' : 'メールアドレスまたはパスワードが間違っています。'})
    return render(request, 'login.html')


def logoutfunc(request):
    logout(request)
    return redirect('meme')


@login_required
def readfunc(request):
    try:
        username = request.user.get_username()
        t =User.objects.filter(username__contains=username).values('last_name')
        user_db = IotModel.objects.filter(token__contains=t)
        df = read_frame(user_db.order_by('-time'), fieldnames=['device', 'time', 'content'])
        dt = [datetime.datetime.fromtimestamp(int(i)) for i in df['time']]
        df['time'] = dt
        html_object = df.to_html(classes='table table-light table-striped table-hover table-bordered table-responsive')
        return render(request, 'detail.html', {'table':html_object ,'username':username})
    except:
        return redirect('login')


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


@login_required
def graphfunc(request):
    try:
        username = request.user.get_username()
        t =User.objects.filter(username__contains=username).values('last_name')
        user_db = IotModel.objects.filter(token__contains=t)
        df = read_frame(user_db.order_by('-time'), fieldnames=['device', 'time', 'content'])
        device_name = df['device'] 
        device_name_set = device_name[~device_name.duplicated()]
        device_time = df['time']
        device_content = df['content']
        device_content_list = [device_content[device_name == i] for i in device_name_set]
        device_time_list = [device_time[device_name == i] for i in device_name_set]
        fig = go.Figure()
        for c,j,n in zip(device_content_list , device_time_list , device_name_set):
            data_y = [float(i.split(',')[0]) for i in np.array(c)]
            data_x = [pd.to_datetime(int(i)+60*60*9, unit='s') for i in np.array(j).flatten()]
            fig.add_trace(go.Scatter(x=data_x, y=data_y, mode='lines+markers',name=str(n)))
        plot_fig = plot(fig, output_type='div', include_plotlyjs=False)
        return render(request, 'graph.html', {'plot_gantt':plot_fig ,'username':username})
    except:
        return redirect('read')


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


def completefunc(request, **kwargs):
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)
    token = kwargs.get('token')
    print(token)
    try:
        user_pk = loads(token, max_age=timeout_seconds)
        print('user_pk:',user_pk)
    except SignatureExpired:
        return HttpResponseBadRequest()
    except BadSignature:
        return HttpResponseBadRequest()
    else:
        try:
            user = User.objects.get(pk=user_pk)
            print('user:',user)
        except User.DoesNotExist:
            return HttpResponseBadRequest()
        else:
            print('user.is_active:',user.is_active)
            user.is_active = True
            user.save()
            return redirect('read')#render(request, 'login.html', {'context' : '登録が完了しました。Complete!'})