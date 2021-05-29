from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout



def loginfunc(request):
    if request.method == "POST":
        email = request.POST['emailadress']
        psw = request.POST['password']
        user = authenticate(request, username=email, password=psw)
        if user is not None:
            login(request, user)
            return redirect('read')
        else:
            return render(request, 'login.html', {'context' : 'メールアドレスまたはパスワードが間違っています。'})
    return render(request, 'login.html')


def logoutfunc(request):
    logout(request)
    return redirect('meme')

