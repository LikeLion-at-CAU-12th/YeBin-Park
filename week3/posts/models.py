from django.db import models
# Create your models here.
#우선 자료보면서 따라해보깅
class Student(models.Model):
    #해당 오브젝트가 무얼 나타내는지 이름을 반환해주는 코드
    def __str__(self):
        return self.name
    #열
    name= models.CharField(default="",max_length=30) #Field의 데이터 타입 문자열,숫자.
    age=models.IntegerField(default=0)
    major= models.CharField(default="",max_length=50)
    gitid=models.CharField(default="",max_length=50) #이제 admin.py에 모델을 등록해야함 #이거 하고 나서 view에도 등록해주자.
