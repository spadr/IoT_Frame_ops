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
        name = email.split('@')
        try :
            user = User.objects.create_user(name[0], email, psw)
            hash = getattr(settings, 'PROJECT_ID', ' ') + secrets.token_hex()
            user.is_active = False
            user.last_name = hash
            user.save()
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
            send_mail(subject, context, from_email, recipient_list)
            return render(request, 'signup.html', {'error' : '登録したメールアドレスへ認証メールを送信しました。URLをクリックして、アカウントを有効化してください。' , 'error2':'Please confirm your email address to complete the registration'})
        except IntegrityError:
            return render(request, 'signup.html', {'error' : 'このユーザーはすでに登録されています。'})
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
            return redirect('read')