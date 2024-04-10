from django.contrib import admin
from .models import Post , Comment

# Register your models here.
admin.site.register(Post) #관리자 페이지에 모델추가
admin.site.register(Comment)
