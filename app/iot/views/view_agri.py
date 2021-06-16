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

from django_pandas.io import read_frame

LIMIT_QUERY = getattr(settings, "LIMIT_QUERY", 10000)

def score_round(val:float, d:int) -> float:
    """
    四捨五入する
    入力:四捨五入したい値val, 四捨五入する桁d
    出力:四捨五入した値
    """
    d -= 1

    p = 10 ** d

    return (val * p * 2 + 1) // 2 / p

def csv2json(df:object) -> object:
    """
    カンマ区切りのデータからからjsonへ変形
    入力:カンマ区切りのデータ, pandas.Dataframe
    出力:json object
    """
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
    return jsons_object

@login_required
def agrifunc(request):
    #ユーザーが登録したデータを取得
    username = request.user.get_username()
    t =User.objects.filter(username__contains=username).values('last_name')
    user_db = IotModel.objects.filter(token__contains=t)

    #クエリ条件 : GHタグ含む
    query = user_db.filter(device__contains='AGRI').order_by('time').reverse()[:LIMIT_QUERY]

    #データが無いとき
    if len(query)==0:
        return render(request, 'nodata.html')
    
    #pandas.DataFrameで読み込み
    df = read_frame(query, fieldnames=['device', 'time', 'content'])

    """CSV形式の場合"""
    jsons_object = csv2json(df)

    #JSONから読み込み
    json_df = pd.read_json(jsons_object)
    col_names = json_df.columns.values.tolist()
    col_names = [col for col in col_names if (col!='Time') and (col!='PositionN') and (col!='PositionX') and (col!='PositionY')]

    #UNIX時間を普通の日時表示に変更
    dt = [datetime.datetime.fromtimestamp(int(i)) for i in json_df['Time']]
    json_df['Time'] = dt
    
    #時間ごとの値の推移を取得
    time_freq = 60
    time_delta = time_freq//60 *-1
    freq = str(time_freq)+'min'
    json_df_N = json_df.groupby('PositionN')
    PositionN = json_df['PositionN'].drop_duplicates().sort_values(ascending=True)
    PositionN_data = [json_df_N.get_group(n) for n in PositionN] #棟ごと
    transitions = [n.groupby(pd.Grouper(key='Time', freq=freq)).mean() for n in PositionN_data] #棟ごとの推移
    hour = datetime.datetime.now() + datetime.timedelta(hours=time_delta)
    latest_datas = [n[n['Time'] >= hour] for n in PositionN_data] #棟ごと時間以内
    
    #グラフ描画
    kinds_of_senser_index = 0
    unit_index =            1
    figure_index =          2
    heatmap_index =         3
    building_name_index =   4
    latest_value_index =    5
    latest_time_index =     6
    kinds_of_building = "Greenhouse"
    building_zero_padding = 2
    figs = [[col_name, [], go.Figure(), [], [], [], [] ] for col_name in col_names]
    for transition,latest_data,pn in zip(transitions,latest_datas,PositionN):
        for fig in figs:
            length = len(latest_data.index)
            unit = ""
            if "(" in fig[kinds_of_senser_index]:
                unit = fig[kinds_of_senser_index].split("(")[-1][:-1]
            if fig[kinds_of_senser_index] not in transition.columns.values.tolist():
                break
            elif length ==0:
                break
            HM_shape = np.array([np.max(latest_data['PositionX']),np.max(latest_data['PositionY'])], dtype=int) + 1
            heatmap = np.zeros(HM_shape)
            heatmap[:,:] = np.nan
            for i,j,k in zip(latest_data[fig[kinds_of_senser_index]],latest_data['PositionX'],latest_data['PositionY']):
                if not np.isnan(i):
                    heatmap[int(j),int(k)] = i
            latest_mean = score_round(np.nanmean(heatmap), 2)
            plot_y = transition[fig[kinds_of_senser_index]]
            plot_x = transition.index
            fig[unit_index].append(unit)
            fig[latest_value_index].append(str(latest_mean))
            fig[latest_time_index].append(latest_data['Time'].iloc[-1].to_pydatetime().strftime("%m/%d %H:%M"))
            name_of_building = kinds_of_building + str(pn).zfill(building_zero_padding)
            fig[building_name_index].append(name_of_building)
            fig[figure_index].add_trace(go.Scatter( x=plot_x, 
                                                    y=plot_y, 
                                                    mode='lines+markers',
                                                    name=name_of_building
                                                    ))
            fig[heatmap_index].append(go.Figure().add_traces(go.Heatmap(z=heatmap, 
                                                                        connectgaps=False, 
                                                                        showlegend=False,
                                                                        colorbar_title_text=fig[kinds_of_senser_index],
                                                                        name=name_of_building
                                                                        )))
    figs = list(zip(*figs))
    kinds_of_senser = figs[kinds_of_senser_index]
    unit_name = figs[unit_index]
    figure_plot = [str(plot(figure, output_type='div', include_plotlyjs=False)) for figure in figs[figure_index]]
    heatmap_plot = [ ''.join([plot(heatmap, output_type='div', include_plotlyjs=False) for heatmap in heatmaps]) for heatmaps in figs[heatmap_index]]
    building_name = figs[building_name_index]
    latest_value = figs[latest_value_index]
    latest_time = figs[latest_time_index]
    output = []
    for sens_num in range(len(kinds_of_senser)):
        a_senser = dict()
        a_senser['kinds_of_senser'] = kinds_of_senser[sens_num]
        a_senser['unit_name'] = unit_name[sens_num]
        a_senser['figure_plot'] = figure_plot[sens_num]
        a_senser['heatmap_plot'] = heatmap_plot[sens_num]
        a_senser['building_name'] = building_name[sens_num]
        a_senser['latest_value'] = latest_value[sens_num]
        a_senser['latest_time'] = latest_time[sens_num]
        output.append(a_senser)
    return render(request, 'agri.html', { 'contents':output,
                                                'username':username,
                                              })