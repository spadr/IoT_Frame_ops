from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

from .models import IotModel

import secrets
import datetime



def datafunc(request, **kwargs):
    #project_idは全アカウントで共通
    project_id = getattr(settings, 'PROJECT_ID')
    content = kwargs.get('contents')
    key = content[0:len(project_id)]

    if secrets.compare_digest(key, project_id):#project_idでkeyの頭部分をチェック
        alluser_last_name = {i['last_name'] for i in User.objects.values('last_name')}

        #カンマの位置でcontentを分割
        posi1 = content.index(',')
        posi2 = content.index(',', posi1+1)
        access_key = content[:posi1]
        device_name = content[posi1+1:posi2]
        list_content = content[posi2+1:]

        if access_key in alluser_last_name:#どのユーザーかチェック
            now_timestamp = int(datetime.datetime.now().timestamp())
            #登録処理
            IotModel.objects.create(token=access_key, device=device_name, time=str(now_timestamp), content=list_content)
            return HttpResponse(now_timestamp)#正常終了のレスポンス
        
        else:
            return HttpResponseBadRequest()#該当ユーザー無しのレスポンス
    
    else:
        return HttpResponseBadRequest()#project_idが一致しない場合のレスポンス


def devfunc(request, **kwargs):
    #project_idは全アカウントで共通
    project_id = getattr(settings, 'PROJECT_ID')
    content = kwargs.get('contents')
    key = content[0:len(project_id)]

    if secrets.compare_digest(key, project_id):#project_idでkeyの頭部分をチェック
        alluser_last_name = {i['last_name'] for i in User.objects.values('last_name')}

        #カンマの位置でcontentを分割
        posi1 = content.index(',')
        posi2 = content.index(',', posi1+1)
        access_key = content[:posi1]
        device_name = content[posi1+1:posi2]
        timestamp = content[posi2+1:posi2+1+10]
        list_content = content[posi2+2+11:]

        if access_key in alluser_last_name:#どのユーザーかチェック
            now_timestamp = int(datetime.datetime.now().timestamp())
            #登録処理
            IotModel.objects.create(token=access_key, device=device_name, time=str(timestamp), content=list_content)
            return HttpResponse(timestamp)#正常終了のレスポンス
        
        else:
            return HttpResponseBadRequest()#該当ユーザー無しのレスポンス
    
    else:
        return HttpResponseBadRequest()#project_idが一致しない場合のレスポンス