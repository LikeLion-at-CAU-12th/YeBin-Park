from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name = 'hello_world'),
    path('page', index, name='my-page'),
    path('<int:id>', get_post_detail, name = "게시글 조회"),
    path('<int:pk>/comments', comment_create, name='comment_create')
]