###Model Serializer case
from rest_framework import serializers
from .models import Post
from .models import Comment
import boto3
from django.conf import settings

class Postserializer(serializers.ModelSerializer):

    class Meta:
        model=Post
        fields="__all__"

        # fields=["writer, content"]등으로 부분만 갖고올 수 있음.

        # exclude =["category"] 이것만 뺴고 갖고 올 수 있음.

        #read_only_fields 도 있음.

    def validate_thumbnail(self, value): 
        if value.name.lower().endswith('.png'):
                raise serializers.ValidationError("png 파일은 업로드가 불가합니다.")
        return value
    

class Commentserializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields="__all__"