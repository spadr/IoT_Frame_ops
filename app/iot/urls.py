from django.contrib import admin
from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', views.signup_user.signupfunc, name='signup'),
    path('complete/<token>/', views.signup_user.completefunc, name='complete'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', views.user.UserApi.as_view(), name='user'),
    path('api/tube/', views.tube.TubeApi.as_view(), name='tube'),
    path('api/element/', views.element.ElementApi.as_view(), name='element'),
    path('api/elements/', views.element.ElementsApi.as_view(), name='elements'),
    path('api/init/', views.init_load.InitApi.as_view(), name='init'),
    path('api/time/', views.time.UnixtimeApi.as_view(), name='time'),
]
