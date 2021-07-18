from django.contrib import admin
from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', views.make_user.signupfunc, name='signup'),
    path('login/', views.sign_user.loginfunc, name='login'),
    path('logout/', views.sign_user.logoutfunc, name='logout'),
    path('read/', views.view_page.readfunc, name='read'),
    path('graph/', views.view_page.graphfunc, name='graph'),
    path('complete/<token>/', views.make_user.completefunc, name='complete'),
    path('agri/', views.view_agri.agrifunc, name='agri'),
    path('', views.view_page.memefunc, name='meme'),
    path('dl/', views.manipulate_data.dlfunc, name='dl'),
    path('delete/', views.manipulate_data.deletefunc, name='delete'),
    path('api/data/', views.create_data.DataReceiveApi.as_view(), name='data'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]