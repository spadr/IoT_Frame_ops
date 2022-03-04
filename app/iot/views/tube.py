
import datetime
import json
import uuid
from django.db import transaction
from iot.models import TubeModel

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from django.utils import timezone

UTC = datetime.timezone(datetime.timedelta(hours=0), 'UTC')


class TubeApi(APIView):
    def get(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        if 'token' in request.GET:
            token = request.GET.get('token')
            queryset = TubeModel.objects.filter(email=request.user, token=token).values(
                "token",
                "name",
                "channel",
                "is_variable",
                "data_type",
                "is_active",
                "monitoring",
                "interval",
                "activity"
            )
        elif 'channel' in request.GET and 'name' in request.GET:
            name = request.GET.get('name')
            channel = request.GET.get('channel')
            queryset = TubeModel.objects.filter(email=request.user, name=name, channel=channel).values(
                "token",
                "name",
                "channel",
                "is_variable",
                "data_type",
                "is_active",
                "monitoring",
                "interval",
                "activity"
            )
        else:
            queryset = TubeModel.objects.filter(email=request.user).values(
                "token",
                "name",
                "channel",
                "is_variable",
                "data_type",
                "is_active",
                "monitoring",
                "interval",
                "activity"
            )

        response_body = {}
        response_body['tube'] = list(queryset)
        response_body['message'] = ''
        response_body['time'] = timestamp
        return Response(response_body, status=HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        tube_token = uuid.uuid4()
        try:
            tube_name = str(decoded['name'])
            tube_channel = str(decoded['channel'])
            tube_type = str(decoded['type'])
        except Exception:
            response_body = {}
            response_body['message'] = 'Jsonの型が不正です。'
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_409_CONFLICT)

        # name&channelはユニーク
        queryset = TubeModel.objects.filter(
            email=request.user, name=tube_name, channel=tube_channel).values()
        if len(queryset) != 0:
            response_body = {}
            response_body['tubes'] = list(queryset)
            response_body['message'] = '既にTubeは存在します。'
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_201_CREATED)

        try:
            tube_isvariable = bool(decoded['isvariable'])
            tube_monitoring = bool(decoded['monitoring'])
            tube_interval = int(decoded['interval'])
        except Exception:
            tube_isvariable = False
            tube_type = tube_type
            tube_monitoring = False
            tube_interval = 60
            TubeModel.objects.create(token=tube_token,
                                     email=request.user,
                                     name=tube_name,
                                     channel=tube_channel,
                                     is_variable=tube_isvariable,
                                     data_type=tube_type,
                                     monitoring=tube_monitoring,
                                     interval=tube_interval,
                                     is_active=False,
                                     activity=timezone.localtime(
                                         datetime.datetime.fromtimestamp(timestamp, UTC))
                                     )
            queryset = TubeModel.objects.filter(email=request.user, name=tube_name, channel=tube_channel).values(
                "token",
                "name",
                "channel",
                "is_variable",
                "data_type",
                "is_active",
                "monitoring",
                "interval",
                "activity"
            )
            response_body = {}
            response_body['tubes'] = list(queryset)
            response_body['message'] = ''
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_201_CREATED)

        # 許可する型
        if all((tube_type != 'number', tube_type != 'boolean', tube_type != 'char')):
            response_body = {}
            response_body['message'] = 'データ型が不正です。入力可能なデータ型はnumber,boolean,charです。'
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_409_CONFLICT)

        try:
            TubeModel.objects.create(token=tube_token,
                                     email=request.user,
                                     name=tube_name,
                                     channel=tube_channel,
                                     is_variable=tube_isvariable,
                                     data_type=tube_type,
                                     monitoring=tube_monitoring,
                                     interval=tube_interval,
                                     is_active=False,
                                     activity=timezone.localtime(
                                         datetime.datetime.fromtimestamp(timestamp, UTC))
                                     )
        except Exception:
            response_body = {}
            response_body['message'] = 'Tubeを追加できませんでした。'
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_409_CONFLICT)
        else:
            queryset = TubeModel.objects.filter(email=request.user, token=tube_token).values(
                "token",
                "name",
                "channel",
                "is_variable",
                "data_type",
                "is_active",
                "monitoring",
                "interval",
                "activity"
            )
            response_body = {}
            response_body['tubes'] = list(queryset)[0]
            response_body['message'] = ''
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_201_CREATED)

    @transaction.atomic
    def put(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        try:
            tube_token = str(decoded['token'])
            tube_name = str(decoded['name'])
            tube_channel = str(decoded['channel'])
            tube_isvariable = bool(decoded['isvariable'])
            tube_monitoring = bool(decoded['monitoring'])
            tube_interval = int(decoded['interval'])
        except Exception:
            return Response(status=HTTP_409_CONFLICT)
        else:
            queryset = TubeModel.objects.filter(
                email=request.user, name=tube_name, channel=tube_channel).values()
            if len(queryset) == 0:
                response_body = {}
                response_body['message'] = '編集可能なTubeは存在しません。'
                response_body['time'] = timestamp
                return Response(response_body, status=HTTP_409_CONFLICT)

        new_token = uuid.uuid4()
        try:
            tube = TubeModel.objects.get(email=request.user, token=tube_token)
            tube.token = new_token
            tube.name = tube_name
            tube.channel = tube_channel
            tube.is_variable = tube_isvariable
            tube.monitoring = tube_monitoring
            tube.interval = tube_interval
            tube.activity = timezone.localtime(
                datetime.datetime.fromtimestamp(timestamp, UTC))
            tube.save()
        except Exception:
            response_body = {}
            response_body['message'] = '編集できませんでした。'
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_409_CONFLICT)
        else:
            queryset = TubeModel.objects.filter(email=request.user, token=new_token).values(
                "token",
                "name",
                "channel",
                "is_variable",
                "data_type",
                "is_active",
                "monitoring",
                "interval",
                "activity"
            )
            response_body = {}
            response_body['tubes'] = list(queryset)
            response_body['message'] = ''
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_201_CREATED)

    @transaction.atomic
    def delete(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        try:
            tube_token = str(decoded['token'])
            tube = TubeModel.objects.get(
                email=request.user, token=tube_token)
            tube.delete()
        except Exception:
            response_body = {}
            response_body['message'] = '削除できませんでした。'
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_409_CONFLICT)
        else:
            response_body = {}
            response_body['message'] = '削除成功'
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_204_NO_CONTENT)
