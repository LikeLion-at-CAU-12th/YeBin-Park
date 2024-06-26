from django.db import models
from django.contrib.auth.models import AbstractUser
from config import settings

class User(AbstractUser): #모델내부함수 구현
    pass

    def get_user_or_none_by_username(username):
        try:
            return User.objects.get(username=username) #get 은 없으면 에러, filter 는 없으면 None 반환.
        except Exception:
            return None

    @staticmethod #email 을 static method 로 지정
    def get_user_or_none_by_email(email):
        try:
            return User.objects.get(email=email) # email 로도 가능
        except Exception:
            return None