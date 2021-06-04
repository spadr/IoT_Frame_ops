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

import json

from decimal import Decimal, ROUND_HALF_UP

from django_pandas.io import read_frame



@login_required
def greenhousefunc(request):
    #ユーザーが登録したデータを取得
    username = request.user.get_username()
    t =User.objects.filter(username__contains=username).values('last_name')
    user_db = IotModel.objects.filter(token__contains=t)

    #クエリ条件 : 一週間以内&GHタグ含む
    now = int(datetime.datetime.now().timestamp())
    last_week = now - 604800
    query = user_db.filter(device__gte=str(last_week)).filter(device__contains='GH')

    #pandas.DataFrameで読み込み
    df = read_frame(query, fieldnames=['device', 'time', 'content'])

    """CSV形式の場合"""
    #--------------------------------------------------------------------------------
    #データの形を整える
    name = df['device'] 
    name_ditinct = name.drop_duplicates()
    time = df['time']
    content = df['content']
    contents = [content[name == i] for i in name_ditinct]
    times = [time[name == i] for i in name_ditinct]

    #メタ情報取得（センサー種類, 設置場所）
    process_type_ = 0
    kind_of_senser_ = 1 
    senser_position_ = 2
    meta_info = []
    for i in name_ditinct:
        info = i.split("-") #[process_type, kinds_of_senser, senser_position]
        kinds_of_senser =  info[kind_of_senser_].split("_")
        senser_position =  list(map(int,info[senser_position_].split("_")))
        meta_info.append([kinds_of_senser, senser_position])
    
    #JSONへ変形
    jsons = []
    position_N = 0 #センサーの場所（棟）
    position_X = 1 #センサーの場所（X軸）
    position_Y = 2 #センサーの場所（Y軸）
    for m,t,c in zip(meta_info,times,contents):#デバイス毎にfor
        senser_position = m[senser_position_-1]
        kinds_of_senser = m[kind_of_senser_-1]
        cast_c = np.array(c)
        cast_t = np.array(t).flatten()
        for y,x in zip(cast_c ,cast_t):
            _json = dict()
            _json["PositionN"] = senser_position[position_N]
            _json["PositionX"] = senser_position[position_X]
            _json["PositionY"] = senser_position[position_Y]
            try:
                num = list(map(float, y.split(',')))
            except:
                pass
            else:
                for n, k in zip(num, kinds_of_senser):
                    _json[k] = n
                    _json["Time"] = str(x)
                jsons.append(_json)
    jsons_object = json.dumps(jsons, indent = 4)
    #--------------------------------------------------------------------------------
    """CSV形式の場合"""

    #JSONから読み込み
    json_df = pd.read_json(jsons_object)
    col_names = json_df.columns.values.tolist()
    col_names = [col for col in col_names if (col!='Time') and (col!='PositionN') and (col!='PositionX') and (col!='PositionY')]

    #UNIX時間を普通の日時表示に変更
    dt = [datetime.datetime.fromtimestamp(int(i)) for i in json_df['Time']]
    json_df['Time'] = dt
    
    #時間ごとの値の推移を取得
    time_freq = '60min'
    json_df_N = json_df.groupby('PositionN')
    PositionN = json_df['PositionN'].drop_duplicates().sort_values(ascending=True)
    transitions = [json_df_N.get_group(n).groupby(pd.Grouper(key='Time', freq=time_freq)).mean() for n in PositionN] #棟ごとの推移
    
    #グラフ描画
    kinds_of_senser_index = 0
    figure_index = 1
    latest_value_index = 2
    latest_time_index = 3
    building_name_index = 4
    kinds_of_building = "Greenhouse"
    building_zero_padding = 2
    figs = [[col_name, go.Figure(), [], [], []] for col_name in col_names]
    for transition,pn in zip(transitions,PositionN):
        for fig in figs:
            if fig[kinds_of_senser_index] not in transition.columns.values.tolist():
                break
            plot_y = transition[fig[kinds_of_senser_index]]
            plot_x = transition.index
            fig[latest_value_index].append(plot_y[-1])#集計データから取るのはおかしい
            fig[latest_time_index].append(plot_x[-1].to_pydatetime().strftime("%m/%d %H:%M"))#集計データから取るのはおかしい
            name_of_building = kinds_of_building + str(pn).zfill(building_zero_padding)
            fig[building_name_index].append(name_of_building)
            fig[1].add_trace(go.Scatter(x=plot_x, y=plot_y, mode='lines+markers',name=name_of_building))
    plot_figs = [[fig[kinds_of_senser_index], plot(fig[figure_index], output_type='div', include_plotlyjs=False)] for fig in figs]
    #plot_figs[0] はセンサーの種類 , plot_figs[1] はグラフ
    
    #html成型=後でTemplate作成=
    plot_html = ""
    for plot_fig in plot_figs:
        unit = ""
        plot_html += '<div class="font-large container row col">'
        sensor_title = '<p>{sensor_name}</p>'
        sensor = plot_fig[kinds_of_senser_index]
        if "(" in sensor:
            unit = " " + sensor.split("(")[-1][:-1]
        sensor_title = sensor_title.format(sensor_name=sensor)
        sensor_figure = plot_fig[figure_index]
        plot_html += sensor_title
        plot_html += '<table class="table bg-light">'
        plot_html += '<thead><tr>'
        for p in fig[building_name_index]:
            plot_html +='<th scope="col" class="table-active">{0}</th>'.format(p)
        plot_html += '</tr></thead>'
        plot_html += '<tbody><tr>'
        for v in fig[latest_value_index]:
            unit_v = str(v) + " " + unit
            plot_html +='<td scope="row">{0}</td table-primary>'.format(unit_v)
        plot_html += '</tr></tbody>'
        plot_html += '<tbody><tr>'
        for t in fig[latest_time_index]:
            plot_html +='<td scope="row" class="table-active">{0}</td>'.format(t)
        plot_html += '</tr></tbody>'
        plot_html += '</table>'
        plot_html += '</div>'
        plot_html += sensor_figure
        plot_html += '<hr>'
    #raise ValueError("error!")
    return render(request, 'greenhouse.html', {'plot_gantts':plot_html ,'username':username})