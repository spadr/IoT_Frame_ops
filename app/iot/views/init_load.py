import datetime

from django.conf import settings
from iot.models import BooleanModel, CharModel, FloatModel, IntModel, TubeModel, User
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
from rest_framework.views import APIView

LIMIT_QUERY = getattr(settings, "LIMIT_QUERY", 10000)
UTC = datetime.timezone(datetime.timedelta(hours=0), "UTC")


class InitApi(APIView):
    def get(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        try:
            usermodel = User.objects.filter(email=request.user).values("email", "is_active", "function_level", "alive_monitoring")
            usermodel = usermodel[0]
        except Exception:
            response_body = {}
            response_body["user"] = []
            response_body["tubes"] = []
            response_body["message"] = "NoUser"
            response_body["time"] = timestamp
            return Response(response_body, status=HTTP_409_CONFLICT)

        try:
            tubemodel = list(
                TubeModel.objects.filter(email=request.user).values(
                    "token", "name", "channel", "is_variable", "data_type", "is_active", "monitoring", "interval", "activity"
                )
            )

            tube_count = len(tubemodel)
            if tube_count == 0:
                response_body = {}
                response_body["user"] = usermodel
                response_body["tubes"] = []
                response_body["message"] = ""
                response_body["time"] = timestamp
                return Response(response_body, status=HTTP_200_OK)

        except Exception:
            response_body = {}
            response_body["user"] = []
            response_body["tubes"] = []
            response_body["message"] = "NoTube"
            response_body["time"] = timestamp
            return Response(response_body, status=HTTP_409_CONFLICT)

        try:
            tubes = [dict(i) for i in tubemodel]
            for tube in tubes:
                data_type = tube["data_type"]
                if data_type == "float":
                    queryset = (
                        FloatModel.objects.filter(tube__email=request.user, tube__token=tube["token"])
                        .order_by("time")
                        .reverse()
                        .select_related()
                        .values("token", "time", "value")[: LIMIT_QUERY // tube_count]
                    )
                    tube["elements"] = list(queryset)
                elif data_type == "int":
                    queryset = (
                        IntModel.objects.filter(tube__email=request.user, tube__token=tube["token"])
                        .order_by("time")
                        .reverse()
                        .select_related()
                        .values("token", "time", "value")[: LIMIT_QUERY // tube_count]
                    )
                    tube["elements"] = list(queryset)
                elif data_type == "boolean":
                    queryset = (
                        BooleanModel.objects.filter(tube__email=request.user, tube__token=tube["token"])
                        .order_by("time")
                        .reverse()
                        .select_related()
                        .values("token", "time", "value")[: LIMIT_QUERY // tube_count]
                    )
                    tube["elements"] = list(queryset)
                elif data_type == "char":
                    queryset = (
                        CharModel.objects.filter(tube__email=request.user, tube__token=tube["token"])
                        .order_by("time")
                        .reverse()
                        .select_related()
                        .values("token", "time", "value")[: LIMIT_QUERY // tube_count]
                    )
                    tube["elements"] = list(queryset)

        except Exception:
            response_body = {}
            response_body["user"] = []
            response_body["tubes"] = []
            response_body["message"] = "NoElement"
            response_body["time"] = timestamp
            return Response(response_body, status=HTTP_409_CONFLICT)

        response_body = {}
        response_body["user"] = usermodel
        response_body["tubes"] = tubes
        response_body["message"] = ""
        response_body["time"] = timestamp
        return Response(response_body, status=HTTP_200_OK)
