from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User

class RegisterSerializer (serializers.ModelSerializer): #Modelserializer 와 그냥 serializer의 차이점은?
    password =serializers.CharField(required=True)
    username=serializers.CharField(required=True)
    email=serializers.CharField(required=True)

    class Meta:
        model=User
        fields =['password', 'username', 'email']
    
    def save(self, request):  # 저장을 위한 데이타. ORM 만들었던 것 처럼 
        user= User.objects.create( #user name 이란 키값을 가지고 와서 생성
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )

        user.set_password(self.validated_data['password']) #password 는 특이하게 저장해줘야한다. 암호화하여 DB에 저장해준다.
        user.save()

        return user
    
    def validate(self,data): #이메일이 중복인지 확인함 -> 중복아니면 validate함
        email=data.get('email', None) #None을 넣어줘서 키값오류 방지

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('email alreadt exists')
        
        return data
    
class AuthSerializer (serializers.ModelSerializer):
    username= serializers.CharField(required=True)
    password=serializers.CharField(required=True)

    class Meta:
        model=User
        fields= ['username','password']

    def validate(self, data):
        username=data.get("username",None)
        password=data.get("password",None)

        user= User.get_user_or_none_by_username(username=username)

        if user is None:   # isNone 과 요 그냥 None 의 차이
            raise serializers.ValidationError("user account not exist")
        else:
            if not user.check_password(raw_password=password):
                raise serializers.ValidationError("wrong password")
            
        token=RefreshToken.for_user(user)
        refresh_token=str(token)
        acces_token =str(token.access_token)

        data={
            "user":user,
            "refresh_token": refresh_token,
            "access_token": acces_token,
        }

        return data
