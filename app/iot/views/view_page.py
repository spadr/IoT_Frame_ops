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


def dict_to_list(dic):
    lst = []
    for e in dic.items():
        lst.extend(e)
    return lst


def memefunc(request):
    host = settings.ALLOWED_HOSTS
    port = 8025
    mailhog_url = 'http://' + host[0] + ':' + str(port) + '/'
    return render(request, 'top.html', {'mailhog_url': mailhog_url})


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