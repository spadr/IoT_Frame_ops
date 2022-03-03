
from django.db import IntegrityError, transaction
from iot.models import User
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import dumps
from django.template.loader import render_to_string
from django.conf import settings

import json

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED
from rest_framework.views import APIView


class UserApi(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)
        queryset = User.objects.filter(email=request.user).values(
            "email",
            "is_active",
            "function_level",
            "alive_monitoring",
            "send_message_to_email",
            "line_token",
            "send_message_to_line",
            "slack_token",
            "slack_channel",
            "send_message_to_slack"
        )
        encoded = queryset[0]

        return Response(encoded, status=HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)

        # superUserのみ
        queryset = User.objects.filter(email=request.user).values()
        encoded = queryset[0]
        if encoded['is_superuser']:
            pass
        else:
            response = {'message': '権限がありません。'}
            return Response(response, status=HTTP_200_OK)

        decoded_body = json.loads(request.body)
        email = decoded_body['email']
        psw = decoded_body['password']

        # ユーザー登録
        try:
            user = User.objects.create_user(email, psw)
        except IntegrityError:
            # ユーザー登録NG
            response = {'message': 'このユーザーはすでに登録されています。'}
            return Response(response, status=HTTP_200_OK)

        try:
            user.is_active = False
            user.save()

        except Exception:
            response = {'message': '登録できません。'}
            return Response(response, status=HTTP_200_OK)

        # 認証メールの作成
        try:
            from_email = settings.EMAIL_ADDRESS
            recipient_list = [email]
            subject = 'Activate Your Account'  # メールタイトル
            current_site = get_current_site(request)
            domain = current_site.domain
            # 内容はtemplateから
            uuid_str = str(user.pk)
            context = render_to_string('account_activation_email.html',
                                       {
                                           'protocol': request.scheme,
                                           'domain': domain,
                                           'token': dumps(uuid_str),
                                           'email': user.email,
                                       })

        except Exception:
            response = {'message': 'メール関係の変数が不正です。'}
            return Response(response, status=HTTP_200_OK)

        # 認証メールの作成
        try:
            send_mail(subject, context, from_email, recipient_list)

        except Exception:
            response = {'message': 'ユーザーの登録は完了しましたが、認証メールの送信に失敗しました。'}
            return Response(response, status=HTTP_200_OK)

        response = {
            'message': '登録したメールアドレスへ認証メールを送信しました。URLをクリックして、アカウントを有効化してください。'}
        return Response(response, status=HTTP_201_CREATED)

    @transaction.atomic
    def put(self, request):
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)
        pass

    @transaction.atomic
    def delete(self, request):
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)
        pass
