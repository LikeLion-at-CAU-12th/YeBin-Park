from django.shortcuts import render
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .serializers import AuthSerializer
from .serializers import OAuthSerializer
from django.contrib.auth import logout
from rest_framework.permissions import IsAuthenticated
from pathlib import Path
import os,json
from django.core.exceptions import ImproperlyConfigured
from allauth.socialaccount.models import SocialAccount

#11주차 소셜로그인

from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured
from .models import User

BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, "secrets.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

GOOGLE_SCOPE_USERINFO = get_secret("GOOGLE_SCOPE_USERINFO")
GOOGLE_REDIRECT = get_secret("GOOGLE_REDIRECT")
GOOGLE_CALLBACK_URI = get_secret("GOOGLE_CALLBACK_URI")
GOOGLE_CLIENT_ID = get_secret("GOOGLE_CLIENT_ID")
GOOGLE_SECRET = get_secret("GOOGLE_SECRET")

from django.shortcuts import redirect
from json import JSONDecodeError
from django.http import JsonResponse
import requests

BASE_URL="http://localhost:8000/"

def google_login(request):
   scope = GOOGLE_SCOPE_USERINFO        # + "https://www.googleapis.com/auth/drive.readonly" 등 scope 설정 후 자율적으로 추가
   return redirect(f"{GOOGLE_REDIRECT}?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

def google_callback(request):
    code = request.GET.get("code")      # Query String 으로 넘어옴
    
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}")

    # token 요청 및 json 변환
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    if error is not None:
        raise JSONDecodeError(error)

    google_access_token = token_req_json.get('access_token') #에러없이 받았음

    email_response = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={google_access_token}")
    res_status = email_response.status_code

    if res_status != 200:
        return JsonResponse({'status': 400,'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    
    email_res_json = email_response.json()
    email = email_res_json.get('email')
    #토큰을 이용해 구글에서 이메일 값을 받아옴.

    serializer = OAuthSerializer(data=email_res_json)

    try:
        #소셜로그인 계정 검증
        user=User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        
        if social_user.provider != 'google':
                return JsonResponse({'error' : "소셜로그인 제공자가 일치하지 않습니다."}, status= 400)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            
            res = JsonResponse(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
        
    #user 에 없을때 회원가입 처리 해주기 (Register View 참고)
    except User.DoesNotExist:

        data={'access_token': google_access_token, 'code': code}
        accept=requests.post(f"{BASE_URL}accounts/google/login/join", data=data)
        accept_status = accept.status_code
        accept_content = accept.content.decode("utf-8")  # 응답 내용을 확인

        if accept_status != 200:
            return JsonResponse({"message": "구글 회원가입 실패", "details": accept_content}, status=accept_status)
        
        user=User.objects.get_or_create(email=email)
        token=RefreshToken.for_user(user)
        refresh_token=str(token)
        access_token=str(token.access_token)

        return Response(
                {
                    "user":serializer.data,
                    "message" :"register success",
                    "token" : {
                        "access_token" :access_token,
                        "refresh_token" : refresh_token,

                    },
                },
                status=status.HTTP_201_CREATED,
            )

    except SocialAccount.DoesNotExist:
        return JsonResponse({'error': '해당 이메일로 등록된 소셜 로그인 계정이 없습니다.'}, status=400)
    

def google_join(request):

    if request.method == 'POST':
        access_token = request.POST.get('access_token')
        code = request.POST.get('code')

        # Google API를 통해 사용자 정보 가져오기
        google_user_info_response = requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}")
        google_user_info = google_user_info_response.json()

        # 가져온 사용자 정보를 기반으로 사용자 생성
        try:
            user_email = google_user_info.get('email', '')
            user_name = google_user_info.get('name', user_email.split('@')[0])  # 이메일 주소를 '@' 기준으로 분할하여 기본 이름으로 사용
            user, created = User.objects.get_or_create(email=google_user_info['email'], username=user_name)

            if created:
                user.save()
                # SocialAccount에 사용자 추가
                SocialAccount.objects.create(provider='google', uid=user.id, user=user)

                # 사용자가 새로 생성되었을 경우에만 토큰 발급
                token = RefreshToken.for_user(user)
                access_token = str(token.access_token)
                refresh_token = str(token)

                return JsonResponse({
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.username
                    },
                    "message": "register success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                }, status=status.HTTP_200_OK)
            else:
                # 이미 존재하는 사용자인 경우
                return JsonResponse({"message": "이미 가입된 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # 사용자 생성 중 오류가 발생한 경우
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # POST 요청이 아닌 경우
        return JsonResponse({"error": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self,request):
        serializer =RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user=serializer.save(request)
            token=RefreshToken.for_user(user)
            refresh_token=str(token)
            access_token=str(token.access_token)
            res=Response(
                {
                    "user":serializer.data,
                    "message" :"register success",
                    "token" : {
                        "access_token" :access_token,
                        "refresh_token" : refresh_token,

                    },
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AuthView(APIView):
    def post(self, request):
        serializer= AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.validated_data["user"]
            access_token=serializer.validated_data["access_token"]
            refresh_token=serializer.validated_data["refresh_token"]
            res =Response(
                {
                    "user" : {
                        "id":user.id,
                        "email": user.email,
                    },
                    "message": "login success",
                    "token": {
                        "access_token" : access_token,
                        "refresh_token" : refresh_token,
                    },
                },
            status=status.HTTP_200_OK,
            )
            res.set_cookie("access_token" ,access_token, httponly=True)
            res.set_cookie("refresh_token", refresh_token, httponly=True)
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LogoutView(APIView):
    permission_classes =[IsAuthenticated]

    def post(self,request):
        logout(request)
        return Response ({"message":"로그아웃됐습니다."}, status=status.HTTP_200_OK)

# Create your views here.
