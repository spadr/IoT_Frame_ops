
import datetime
import json
import uuid
from django.db import transaction
from iot.models import NumberModel, BooleanModel, CharModel, TubeModel
from django.conf import settings

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_406_NOT_ACCEPTABLE
from rest_framework.views import APIView

from django.utils import timezone

LIMIT_QUERY = getattr(settings, "LIMIT_QUERY", 10000)
UTC = datetime.timezone(datetime.timedelta(hours=0), 'UTC')


class ElementApi(APIView):
    def get(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        if 'tube_token' in request.GET:
            # paramが指定されている場合の処理
            tube_token = request.GET.get('tube_token')
            tube = TubeModel.objects.get(
                email=request.user, token=tube_token)
            number_queryset = NumberModel.objects.filter(tube__email=request.user, tube__id=tube.id).order_by(
                'time').reverse().select_related().values('tube__channel', 'tube__name', 'tube__token', 'token', 'time', 'element')[:LIMIT_QUERY]
            boolean_queryset = BooleanModel.objects.filter(tube__email=request.user, tube__id=tube.id).order_by(
                'time').reverse().select_related().values('tube__channel', 'tube__name', 'tube__token', 'token', 'time', 'element')[:LIMIT_QUERY]
            char_queryset = CharModel.objects.filter(tube__email=request.user, tube__id=tube.id).order_by(
                'time').reverse().select_related().values('tube__channel', 'tube__name', 'tube__token', 'token', 'time', 'element')[:LIMIT_QUERY]

        else:
            tube_count = len(TubeModel.objects.filter(email=request.user).distinct(
                'channel').order_by('channel').values_list('channel', flat=True))
            if tube_count == 0:
                response_body = {}
                response_body['number'] = []
                response_body['boolean'] = []
                response_body['char'] = []
                response_body['message'] = ''
                response_body['time'] = timestamp
                return Response(response_body, status=HTTP_200_OK)

            number_queryset = NumberModel.objects.filter(tube__email=request.user).order_by(
                'time').reverse().select_related().values('tube__channel', 'tube__name', 'tube__token', 'token', 'time', 'element')[:LIMIT_QUERY//tube_count]
            boolean_queryset = BooleanModel.objects.filter(tube__email=request.user).order_by(
                'time').reverse().select_related().values('tube__channel', 'tube__name', 'tube__token', 'token', 'time', 'element')[:LIMIT_QUERY//tube_count]
            char_queryset = CharModel.objects.filter(tube__email=request.user).order_by(
                'time').reverse().select_related().values('tube__channel', 'tube__name', 'tube__token', 'token', 'time', 'element')[:LIMIT_QUERY//tube_count]

        response_body = {}
        response_body['number'] = list(number_queryset)
        response_body['boolean'] = list(boolean_queryset)
        response_body['char'] = list(char_queryset)
        response_body['message'] = ''
        response_body['time'] = timestamp
        return Response(response_body, status=HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        tube_token = str(decoded['token'])
        element_time = int(decoded['time'])
        tube = TubeModel.objects.get(email=request.user, token=tube_token)
        try:
            if tube.data_type == 'number':
                element_value = float(decoded['element'])
                NumberModel.objects.create(tube=tube,
                                           time=timezone.localtime(
                                               datetime.datetime.fromtimestamp(element_time, UTC)),
                                           element=element_value
                                           )
            elif tube.data_type == 'boolean':
                element_value = bool(decoded['element'])
                BooleanModel.objects.create(tube=tube,
                                            time=timezone.localtime(
                                                datetime.datetime.fromtimestamp(element_time, UTC)),
                                            element=element_value
                                            )
            elif tube.data_type == 'char':
                element_value = str(decoded['element'])
                CharModel.objects.create(tube=tube,
                                         time=timezone.localtime(
                                             datetime.datetime.fromtimestamp(element_time, UTC)),
                                         element=element_value
                                         )

        except Exception:
            return Response(status=HTTP_406_NOT_ACCEPTABLE)
        else:
            response_body = {}
            response_body['message'] = ''
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_200_OK)

    @transaction.atomic
    def put(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        try:
            element_time = int(decoded['time'])
        except Exception:
            element_time = None

        try:
            element_value = decoded['element']
        except Exception:
            element_value = None

        try:
            tube_token = str(decoded['tube__token'])
            elem_token = str(decoded['token'])
            tube = TubeModel.objects.get(email=request.user, token=tube_token)

            if tube.data_type == 'number':
                ele = NumberModel.objects.get(token=elem_token)
                ele.token = uuid.uuid4()
                if element_value is not None:
                    ele.element = float(decoded['element'])

                if element_time is not None:
                    ele.time = timezone.localtime(
                        datetime.datetime.fromtimestamp(element_time, UTC))

                ele.save()

            elif tube.data_type == 'boolean':
                ele = BooleanModel.objects.get(token=elem_token)
                ele.token = uuid.uuid4()
                if element_value is not None:
                    ele.element = bool(decoded['element'])

                if element_time is not None:
                    ele.time = timezone.localtime(
                        datetime.datetime.fromtimestamp(element_time, UTC))

                ele.save()

            elif tube.data_type == 'char':
                ele = CharModel.objects.get(token=elem_token)
                ele.token = uuid.uuid4()
                if element_value is not None:
                    ele.element = str(decoded['element'])

                if element_time is not None:
                    ele.time = timezone.localtime(
                        datetime.datetime.fromtimestamp(element_time, UTC))

                ele.save()

        except Exception:
            response_body = {}
            response_body['message'] = '変更できませんでした。'
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_406_NOT_ACCEPTABLE)

        else:
            response_body = {}
            response_body['message'] = ''
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_200_OK)

    @transaction.atomic
    def delete(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        try:
            tube_token = str(decoded['tube__token'])
            elem_token = str(decoded['token'])
            tube = TubeModel.objects.get(email=request.user, token=tube_token)

            if tube.data_type == 'number':
                ele = NumberModel.objects.get(token=elem_token)
                ele.delete()

            elif tube.data_type == 'boolean':
                ele = BooleanModel.objects.get(token=elem_token)
                ele.delete()

            elif tube.data_type == 'char':
                ele = CharModel.objects.get(token=elem_token)
                ele.delete()

        except Exception:
            response_body = {}
            response_body['message'] = '削除できませんでした。'
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_406_NOT_ACCEPTABLE)

        else:
            response_body = {}
            response_body['message'] = ''
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_200_OK)


class ElementsApi(APIView):
    @transaction.atomic
    def post(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        for packet in decoded['content']:
            try:
                tube_token = str(packet['token'])
                element_time = int(packet['time'])
                tube = TubeModel.objects.get(
                    email=request.user, token=tube_token)
                if tube.data_type == 'number':
                    element_value = float(packet['value'])
                    NumberModel.objects.create(tube=tube,
                                               time=timezone.localtime(
                                                   datetime.datetime.fromtimestamp(element_time, UTC)),
                                               element=element_value
                                               )
                elif tube.data_type == 'boolean':
                    element_value = bool(packet['value'])
                    BooleanModel.objects.create(tube=tube,
                                                time=timezone.localtime(
                                                    datetime.datetime.fromtimestamp(element_time, UTC)),
                                                element=element_value
                                                )
                elif tube.data_type == 'char':
                    element_value = str(packet['value'])
                    CharModel.objects.create(tube=tube,
                                             time=timezone.localtime(
                                                 datetime.datetime.fromtimestamp(element_time, UTC)),
                                             element=element_value
                                             )
            except Exception:
                pass
        else:
            response_body = {}
            response_body['message'] = ''
            response_body['time'] = timestamp
            return Response(response_body, status=HTTP_200_OK)
