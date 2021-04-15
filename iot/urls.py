from django.contrib import admin
from django.urls import path
from .views import signupfunc, graphfunc , loginfunc, logoutfunc, readfunc, completefunc, datafunc, memefunc, dlfunc, deletefunc

urlpatterns = [
    path('signup/', signupfunc, name='signup'),
    path('login/', loginfunc, name='login'),
    path('logout/', logoutfunc, name='logout'),
    path('read/', readfunc, name='read'),
    path('graph/', graphfunc, name='graph'),
    path('complete/<token>/', completefunc, name='complete'),
    path('data/<contents>/', datafunc, name='data'),
    path('', memefunc, name='meme'),
    path('dl/', dlfunc, name='dl'),
    path('delete/', deletefunc, name='delete'),
]
