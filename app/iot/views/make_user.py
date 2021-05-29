from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponseBadRequest

import secrets


def signupfunc(request):
    if request.method == "POST":
        email = request.POST['emailadress']
        psw = request.POST['password']

        try :
            user = User.objects.create_user(email, email, psw)
        except :
            return render(request, 'signup.html', {'error' : 'このユーザーはすでに登録されています。'})
        
        try:
            hash = getattr(settings, 'PROJECT_ID', ' ') + secrets.token_hex()
            user.is_active = False
            user.last_name = hash
            user.save()
        except :
            return render(request, 'signup.html', {'error' : 'DBへの入力値が不正です。'})
        
        try:
            from_email = 'EMAIL_ADDRESS'
            recipient_list = [email]
            subject = 'Activate Your Account'
            current_site = get_current_site(request)
            domain = current_site.domain
            context = render_to_string('account_activation_email.html',{
                'protocol': request.scheme,
                'domain': domain,
                'token': dumps(user.pk),
                'user': user,
                'hash': hash,
            })
        except :
            return render(request, 'signup.html', {'error' : 'メール関係の変数が不正です。'})
        
        try:
            send_mail(subject, context, from_email, recipient_list)
            return render(request, 'signup.html', {'error' : '登録したメールアドレスへ認証メールを送信しました。URLをクリックして、アカウントを有効化してください。' , 'error2':'Please confirm your email address to complete the registration'})
        except :
            return render(request, 'signup.html', {'error' : 'ユーザーの登録は完了しましたが、認証メールを送信に失敗しました。' , 'error2':'入力したメールアドレスを再度ご確認の上、管理者にお問い合わせください。'})
    
    return render(request, 'signup.html')



def completefunc(request, **kwargs):
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)
    token = kwargs.get('token')
    try:
        user_pk = loads(token, max_age=timeout_seconds)
        print('user_pk:',user_pk)
    except SignatureExpired:
        return HttpResponseBadRequest()
    except BadSignature:
        return HttpResponseBadRequest()
    else:
        try:
            user = User.objects.get(pk=user_pk)
            print('user:',user)
        except User.DoesNotExist:
            return HttpResponseBadRequest()
        else:
            print('user.is_active:',user.is_active)
            user.is_active = True
            user.save()
            return redirect('meme')
