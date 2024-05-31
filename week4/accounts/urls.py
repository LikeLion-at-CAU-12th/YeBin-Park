from django.urls import path
from .views import *
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns= [
    path("join/", RegisterView.as_view()),
    path("login/", AuthView.as_view()),
    path("logout/", LogoutView.as_view()),

    path("token/",TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("google/login/",google_login, name="google_login"), # 프론트가 연결해줄땐 삭제가능
    path("google/callback/", google_callback, name="google_callback"),
    path("google/login/join", google_join, name='google_login_join'),
]