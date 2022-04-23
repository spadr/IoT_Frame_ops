import datetime
import json
import uuid

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from iot.models import BooleanModel, CharModel, FloatModel, ImageModel, IntModel, TubeModel
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from rest_framework.views import APIView

LIMIT_QUERY = getattr(settings, "LIMIT_QUERY", 10000)
UTC = datetime.timezone(datetime.timedelta(hours=0), "UTC")


class ElementApi(APIView):
    def get(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        if "token" in request.GET and "length" in request.GET:
            # paramが指定されている場合の処理
            tube_token = request.GET.get("token")
            element_length = int(request.GET.get("length"))
            element_length = min([element_length, LIMIT_QUERY])
            tube = TubeModel.objects.get(email=request.user, token=tube_token)
            float_queryset = (
                FloatModel.objects.filter(tube__email=request.user, tube__id=tube.id)
                .order_by("time")
                .reverse()
                .select_related()
                .values("token", "time", "value")[:element_length]
            )
            int_queryset = (
                IntModel.objects.filter(tube__email=request.user, tube__id=tube.id)
                .order_by("time")
                .reverse()
                .select_related()
                .values("token", "time", "value")[:element_length]
            )
            boolean_queryset = (
                BooleanModel.objects.filter(tube__email=request.user, tube__id=tube.id)
                .order_by("time")
                .reverse()
                .select_related()
                .values("token", "time", "value")[:element_length]
            )
            char_queryset = (
                CharModel.objects.filter(tube__email=request.user, tube__id=tube.id)
                .order_by("time")
                .reverse()
                .select_related()
                .values("token", "time", "value")[:element_length]
            )

        else:
            tube_count = len(TubeModel.objects.filter(email=request.user).distinct("channel").order_by("channel").values_list("channel", flat=True))
            if tube_count == 0:
                response_body = {}
                response_body["number"] = []
                response_body["boolean"] = []
                response_body["char"] = []
                response_body["message"] = ""
                response_body["time"] = timestamp
                return Response(response_body, status=HTTP_200_OK)

            float_queryset = (
                FloatModel.objects.filter(tube__email=request.user)
                .order_by("time")
                .reverse()
                .select_related()
                .values("token", "time", "value")[: LIMIT_QUERY // tube_count]
            )
            int_queryset = (
                IntModel.objects.filter(tube__email=request.user)
                .order_by("time")
                .reverse()
                .select_related()
                .values("token", "time", "value")[: LIMIT_QUERY // tube_count]
            )
            boolean_queryset = (
                BooleanModel.objects.filter(tube__email=request.user)
                .order_by("time")
                .reverse()
                .select_related()
                .values("token", "time", "value")[: LIMIT_QUERY // tube_count]
            )
            char_queryset = (
                CharModel.objects.filter(tube__email=request.user)
                .order_by("time")
                .reverse()
                .select_related()
                .values("token", "time", "value")[: LIMIT_QUERY // tube_count]
            )

        response_body = {}
        response_body["float"] = list(float_queryset)
        response_body["int"] = list(int_queryset)
        response_body["boolean"] = list(boolean_queryset)
        response_body["char"] = list(char_queryset)
        response_body["message"] = ""
        response_body["time"] = timestamp
        return Response(response_body, status=HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        tube_token = str(decoded["token"])
        element_time = int(decoded["time"])
        try:
            tube = TubeModel.objects.get(email=request.user, token=tube_token)
            tube.activity = timezone.localtime(datetime.datetime.fromtimestamp(timestamp, UTC))
            tube.save()
            if tube.data_type == "float":
                element_value = float(decoded["value"])
                FloatModel.objects.create(tube=tube, time=timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC)), value=element_value)
            elif tube.data_type == "int":
                element_value = float(decoded["value"])
                IntModel.objects.create(tube=tube, time=timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC)), value=element_value)
            elif tube.data_type == "boolean":
                element_value = bool(decoded["value"])
                BooleanModel.objects.create(tube=tube, time=timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC)), value=element_value)
            elif tube.data_type == "char":
                element_value = str(decoded["value"])
                CharModel.objects.create(tube=tube, time=timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC)), value=element_value)

        except Exception:
            return Response(status=HTTP_409_CONFLICT)
        else:
            response_body = {}
            response_body["message"] = ""
            response_body["time"] = timestamp
            return Response(response_body, status=HTTP_201_CREATED)

    @transaction.atomic
    def put(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        try:
            element_time = int(decoded["time"])
        except Exception:
            element_time = None

        try:
            element_value = decoded["value"]
        except Exception:
            element_value = None

        try:
            tube_token = str(decoded["tube__token"])
            elem_token = str(decoded["token"])
            tube = TubeModel.objects.get(email=request.user, token=tube_token)

            if tube.data_type == "float":
                ele = FloatModel.objects.get(token=elem_token)
                ele.token = uuid.uuid4()
                if element_value is not None:
                    ele.element = float(decoded["value"])

                if element_time is not None:
                    ele.time = timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC))

                ele.save()

            elif tube.data_type == "int":
                ele = IntModel.objects.get(token=elem_token)
                ele.token = uuid.uuid4()
                if element_value is not None:
                    ele.element = float(decoded["value"])

                if element_time is not None:
                    ele.time = timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC))

                ele.save()

            elif tube.data_type == "boolean":
                ele = BooleanModel.objects.get(token=elem_token)
                ele.token = uuid.uuid4()
                if element_value is not None:
                    ele.element = bool(decoded["value"])

                if element_time is not None:
                    ele.time = timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC))

                ele.save()

            elif tube.data_type == "char":
                ele = CharModel.objects.get(token=elem_token)
                ele.token = uuid.uuid4()
                if element_value is not None:
                    ele.element = str(decoded["value"])

                if element_time is not None:
                    ele.time = timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC))

                ele.save()

        except Exception:
            response_body = {}
            response_body["message"] = "変更できませんでした。"
            response_body["time"] = timestamp
            return Response(response_body, status=HTTP_409_CONFLICT)

        else:
            response_body = {}
            response_body["message"] = ""
            response_body["time"] = timestamp
            return Response(response_body, status=HTTP_201_CREATED)

    @transaction.atomic
    def delete(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        try:
            tube_token = str(decoded["tube__token"])
            elem_token = str(decoded["token"])
            tube = TubeModel.objects.get(email=request.user, token=tube_token)

            if tube.data_type == "float":
                ele = FloatModel.objects.get(token=elem_token)
                ele.delete()

            elif tube.data_type == "int":
                ele = IntModel.objects.get(token=elem_token)
                ele.delete()

            elif tube.data_type == "boolean":
                ele = BooleanModel.objects.get(token=elem_token)
                ele.delete()

            elif tube.data_type == "char":
                ele = CharModel.objects.get(token=elem_token)
                ele.delete()

        except Exception:
            response_body = {}
            response_body["message"] = "削除できませんでした。"
            response_body["time"] = timestamp
            return Response(response_body, status=HTTP_409_CONFLICT)

        else:
            response_body = {}
            response_body["message"] = ""
            response_body["time"] = timestamp
            return Response(response_body, status=HTTP_204_NO_CONTENT)


class ElementsApi(APIView):
    @transaction.atomic
    def post(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        decoded = json.loads(request.body)
        for packet in decoded["content"]:
            tube_token = str(packet["token"])
            element_time = int(packet["time"])

            try:
                tube = TubeModel.objects.get(email=request.user, token=tube_token)
                tube.activity = timezone.localtime(datetime.datetime.fromtimestamp(timestamp, UTC))
                tube.save()
                if tube.data_type == "float":
                    element_value = float(packet["value"])
                    FloatModel.objects.create(tube=tube, time=timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC)), value=element_value)
                elif tube.data_type == "int":
                    element_value = float(packet["value"])
                    IntModel.objects.create(tube=tube, time=timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC)), value=element_value)
                elif tube.data_type == "boolean":
                    element_value = bool(packet["value"])
                    BooleanModel.objects.create(tube=tube, time=timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC)), value=element_value)
                elif tube.data_type == "char":
                    element_value = str(packet["value"])
                    CharModel.objects.create(tube=tube, time=timezone.localtime(datetime.datetime.fromtimestamp(element_time, UTC)), value=element_value)
            except Exception:
                response_body = {}
                response_body["message"] = "登録できませんでした。"
                response_body["time"] = timestamp
                return Response(response_body, status=HTTP_409_CONFLICT)
        else:
            response_body = {}
            response_body["message"] = ""
            response_body["time"] = timestamp
            return Response(response_body, status=HTTP_201_CREATED)
