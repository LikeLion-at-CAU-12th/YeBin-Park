from django.urls import path
from posts.views import *

urlpatterns = [
    # path('', hello_world, name = 'hello_world'),
    path('page', index, name='my-page'),
    # path('<int:id>', get_post_detail, name = "게시글 조회"),
    path('', post_list, name="post_list"),
    path('<int:id>/', post_detail, name='post_detail'),
    path('<int:id>/comments/', comment_list, name='comment_list'),
    path('found/', post_found,name='post_found')
]