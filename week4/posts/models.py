from django.db import models
from django.conf import settings
from accounts.models import User

## 추상 클래스 정의
class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract = True

class Post(BaseModel):

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="제목", max_length=20)
    content = models.TextField(verbose_name="내용")
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, db_column="writer", null=True)
    category = models.CharField(choices=CHOICES, max_length=20)

    objects=models.Manager()

class Comment(BaseModel):

    id= models.AutoField(primary_key=True)
    post=models.ForeignKey(Post, on_delete=models.CASCADE) #CASCADE 로 post가 삭제되면 comment도 삭제되도록 한다.
    content = models.TextField(verbose_name="내용")
    user = models.CharField(verbose_name="작성자", max_length=10)

    def __str__(self):
        return self.content
