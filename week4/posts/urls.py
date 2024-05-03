from django.urls import path
from posts.views import *

urlpatterns = [
    # path('', hello_world, name = 'hello_world'),
    path('page', index, name='my-page'),
    # path('<int:id>', get_post_detail, name = "게시글 조회"),
    
    #path('', post_list, name="post_list"),
    #path('<int:id>/', post_detail, name='post_detail'),
    #path('<int:id>/comments/', comment_list, name='comment_list'),
    path('found/', post_found,name='post_found'),

    # 7주차 이후 링크
    path('',PostList.as_view()),
    path('<int:id>',PostDetail.as_view()),
    path('<int:id>/comments/',CommentDetail.as_view()), #이때 id는 댓글이 달린post id를 써야한다.
    path('<int:post_id>/comments/<int:comment_id>',CommentDetail.as_view()), #이때 id는 댓글이 달린post id에 지우려는 comment의 id 까지 작성한다.

]