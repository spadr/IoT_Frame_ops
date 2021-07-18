from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

from .models import IotModel

import secrets
import datetime
import json

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.views import APIView


class DataReceiveApi(APIView):
    def get(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_200_OK)
    
    def post(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())

        if not request.user.is_authenticated:
                return Response(status=HTTP_401_UNAUTHORIZED)
        
        datas = json.loads(request.body)
        access_key = datas['key']
        project_id = getattr(settings, 'PROJECT_ID')
        project_key =access_key[0:len(project_id)]
        content = datas['content']
        packet_len = len(content)

        if secrets.compare_digest(project_key, project_id):#project_idでkeyの頭部分をチェック
            alluser_last_name = {i['last_name'] for i in User.objects.values('last_name')}
            if access_key in alluser_last_name:#どのユーザーかチェック
                for packet_num in range(packet_len):
                    packet = content[str(packet_num)]
                    sensor_name = packet['name']
                    sensor_channel = packet['channel']
                    sensor_time = packet['time']
                    sensor_data = packet['data']
                    sensor_type = packet['type']
                    
                    #登録処理
                    IotModel.objects.create(long_id=str(access_key), 
                                            name=str(sensor_name), 
                                            time=datetime.datetime.fromtimestamp(int(sensor_time), datetime.timezone(datetime.timedelta(hours=9))),
                                            channel =str(sensor_channel),
                                            type =str(sensor_type),
                                            data=str(sensor_data))
                
                response = {'time': now_timestamp}
                return Response(response, status=HTTP_201_CREATED)#正常終了のレスポンス
            
            else:
                return Response(status=HTTP_401_UNAUTHORIZED)#該当ユーザー無しのレスポンス
        
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)#project_idが一致しない場合のレスポンス