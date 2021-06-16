from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.make_user.signupfunc, name='signup'),
    path('login/', views.sign_user.loginfunc, name='login'),
    path('logout/', views.sign_user.logoutfunc, name='logout'),
    path('read/', views.view_page.readfunc, name='read'),
    path('graph/', views.view_page.graphfunc, name='graph'),
    path('complete/<token>/', views.make_user.completefunc, name='complete'),
    path('data/<contents>/', views.create_data.datafunc, name='data'),
    path('dev/<contents>/', views.create_data.devfunc, name='dev'),
    path('agri/', views.view_agri.agrifunc, name='agri'),
    path('', views.view_page.memefunc, name='meme'),
    path('dl/', views.manipulate_data.dlfunc, name='dl'),
    path('delete/', views.manipulate_data.deletefunc, name='delete'),
]