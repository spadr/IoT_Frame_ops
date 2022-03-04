
import datetime


from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


class UnixtimeApi(APIView):
    def get(self, request):
        timestamp = int(datetime.datetime.now().timestamp())
        response_body = {}
        response_body['message'] = ''
        response_body['time'] = timestamp
        return Response(response_body, status=HTTP_200_OK)
