from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import IotModel

import plotly.graph_objects as go
from plotly.offline import plot

import numpy as np
import pandas as pd

import datetime

from django_pandas.io import read_frame

LIMIT_QUERY = getattr(settings, "LIMIT_QUERY", 10000)

def memefunc(request):
    host = settings.ALLOWED_HOSTS
    port = 8025#docker-compose.ymlで設定したmailhog_urlのHTTPポート

    mailhog_url = 'http://' + host[0] + ':' + str(port) + '/'

    return render(request, 'top.html', {'mailhog_url': mailhog_url})


@login_required
def readfunc(request):
    #ユーザーが登録したデータを取得
    username = request.user.get_username()
    t =User.objects.filter(username__contains=username).values('last_name')
    user_db = IotModel.objects.filter(token__contains=t).order_by('time').reverse()[:LIMIT_QUERY]
    df = read_frame(user_db, fieldnames=['device', 'time', 'content'])

    #UNIX時間を普通の日時表示に変更
    dt = [datetime.datetime.fromtimestamp(int(i)) for i in df['time']]
    df['time'] = dt

    html_object = df.to_html(classes='table table-light table-striped table-hover table-bordered table-responsive')

    return render(request, 'detail.html', {'table':html_object ,'username':username})



@login_required
def graphfunc(request):
    #ユーザーが登録したデータを取得
    username = request.user.get_username()
    t =User.objects.filter(username__contains=username).values('last_name')
    user_db = IotModel.objects.filter(token__contains=t).order_by('time').reverse()[:LIMIT_QUERY]

    #クエリ
    df = read_frame(user_db, fieldnames=['device', 'time', 'content'])
    
    #データの形を整える
    device_name = df['device'] 
    device_name_set = device_name.drop_duplicates()
    device_time = df['time']
    device_content = df['content']
    device_content_list = [device_content[device_name == i] for i in device_name_set]
    device_time_list = [device_time[device_name == i] for i in device_name_set]
    
    #グラフ描画
    fig = go.Figure()
    for c,j,n in zip(device_content_list , device_time_list , device_name_set):#デバイス毎にfor
        data_y = []
        data_x = []
        for y,x in zip(np.array(c),np.array(j).flatten()):
            #数値以外が登録されていた場合は無視
            try:
                num = float(y.split(',')[0])#最初の数字をグラフに表示
                data_y.append(num)
            except:
                pass
            else:
                time = pd.to_datetime(int(x)+60*60*9, unit='s')#日本時間UTC+9
                data_x.append(time)
        
        fig.add_trace(go.Scatter(x=data_x, y=data_y, mode='lines+markers',name=str(n)))
    
    plot_fig = plot(fig, output_type='div', include_plotlyjs=False)

    return render(request, 'graph.html', {'plot_gantt':plot_fig ,'username':username})