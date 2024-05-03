# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
from .forms import CommentForm
from .models import Post , Comment
import json
from .serializers import Postserializer
from .serializers import Commentserializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework import status
from django.http import Http404

class PostList(APIView):
    def post(self,request, format=None):
        serializer = Postserializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        posts=Post.objects.all()
        serializers=Postserializer(posts, many=True)
        return Response(serializers.data)
    

class PostDetail(APIView):
    def get(self, request, id):
        post= get_object_or_404(Post, id=id)
        serializer=Postserializer(post)
        return Response(serializer.data)
    
    def put(self, request, id):
        post=get_object_or_404(Post, id=id)
        serializer=Postserializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        post=get_object_or_404(Post, id=id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentDetail(APIView):
    def get(self, request, id): #포스트의 아이디를 받아 해당 포스트의 id 보여줌.
        callpost=Post.objects.get(pk=id)
        comment_filter= Comment.objects.filter(post=callpost.id)
        serializer=Commentserializer(comment_filter, many=True)
        return Response(serializer.data)

    def post(self, request,id):
        callpost=Post.objects.get(pk=id)
        serializer=Commentserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=callpost)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id, comment_id):
        comment=Comment.objects.filter(pk=comment_id, post_id=post_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




#DRF 적용하기 전
# Create your views here.
#7주차 이전 내용들
@require_http_methods(["POST","GET"]) # 게시글 생성, 목록 조회
def post_list(request):

    if request.method=="POST":
        body = json.loads(request.body.decode('utf-8'))
        # 데이터 생성해주기
        new_post= Post.objects.create(
            writer=body['writer'],
            title=body['title'],
            content=body['content'],
            category=body['category']
        )

        new_post_json ={
            'id' : new_post.id,
            'writer' : new_post.writer,
            'title' : new_post.title,
            'content': new_post.content,
            'category' :new_post.category
        }

        return JsonResponse({
            'status' :200,
            'message': "게시글 조회 성공",
            'data' : new_post_json
        })
    
    if request.method== "GET":
        post_all= Post.objects.all()

        #JSon 형식으로 변환하여 리스트로 저장.
        post_json_all =[]

        for post in post_all:
            post_json={
                "id" : post.id,
                "title" :post.writer,
                "content" :post.content,
                "category" :post.category
            }
            post_json_all.append(post_json)
        
        return JsonResponse({
            'status' :200,
            'message': "게시글 목록 조회 성공",
            'data' : post_json_all
        })
    
@require_http_methods(["GET", "PATCH" , "DELETE"]) #게시글 읽어오기, 수정, 삭제하기
def post_detail(request, id):
    if request.method == "GET":
        post= get_object_or_404(Post, pk=id)

        post_json={
            "id" : post.id,
            "title" :post.writer,
            "content" :post.content,
            "category" :post.category
        }

        return JsonResponse ({
        'status' :200,
        'message': "게시글 조회 성공",
        'data' : post_json
        })

    if request.method=="PATCH":
        body=json.loads(request.body.decode('utf-8'))

        update_post=get_object_or_404(Post,pk=id)

        update_post.title=body['title']
        update_post.content=body['content']
        update_post.category= body['category']

        update_post.save()

        update_post_json={
            "id" :update_post.id,
            "wrtier" :update_post.writer,
            "content" : update_post.content,
            "title" : update_post.title,
            "category" : update_post.category
        }

        return JsonResponse ({
            'status' :200,
            'message' :'게시글 수정 성공',
            'data' : update_post_json
        })
    
    if request.method=="DELETE":
        delete_post =get_object_or_404(Post, pk=id)

        delete_post.delete()

        return JsonResponse ({
            'status' :200,
            'message' :'게시글 삭제  성공',
            'data' : None
        })
    

# 코멘트 관련 함수 -> 클래스뷰로 바꿀것

@require_http_methods(["GET", "POST"]) # 스탠다드 과제. 글에 해당하는 댓글목록 조회. 포스트목록조회 코드참고. 하는김에 POST까지.
def comment_list(request, id):
    if request.method == "GET": # 댓글 가져오기 (해당되는 포스트에 있는 댓글들)
        callpost=Post.objects.get(pk=id) #호출할 post의 id를 먼저 받고 이에 해당되는 comment 필터링으로 받기.
        comment_filter= Comment.objects.filter(post=callpost.id)
        comment_json_filter=[] #댓글 여러개니까 배열만들고

        for comment in comment_filter: # comment_all에는 필터링된 comment들이 담겨있고, 이를 제이슨 형식으로 리스트에 옮겨주기.
            comment_json={
                "id" : comment.id,
                "content" :comment.content,
                "user" :comment.user,
                "create" : comment.created_at                
            }
            comment_json_filter.append(comment_json)
        
        return JsonResponse({
            'status' :200,
            'message': "댓글 목록 조회 성공",
            'data' : comment_json_filter
        },json_dumps_params={'ensure_ascii': False})
    
    if request.method=="POST": #댓글 생성하기
        posts=Post.objects.get(pk=id)
        body = json.loads(request.body.decode('utf-8'))
        # 데이터 생성해주기
        new_comment= Comment.objects.create(
            user=body['user'],
            content=body['content'],
            post_id=id
        )

        new_comment_json ={
            'id' : new_comment.id,
            'post' :posts.id,
            'user' : new_comment.user,
            'content': new_comment.content
        }

        return JsonResponse({
            'status' :200,
            'message': "댓글 생성 성공",
            'data' : new_comment_json
        },json_dumps_params={'ensure_ascii': False})


# 완전초기 함수
    
@require_http_methods(["GET"]) # 게시글 생성, 목록 조회
def post_found(request):

    if request.method== "GET":
        post_all= Post.objects.filter(created_at__range=['2024-04-04','2024-04-10']).order_by('-created_at')
        #post_all= Post.objects.filter(created_at__range=[date.today() - timedelta(days=6), date.today()]).orderby('-created_at')
        #위 코드는 최근 일주일을 받을 수 있는코드.

        #JSon 형식으로 변환하여 리스트로 저장
        post_json_all =[]

        for post in post_all:
            post_json={
                "id" : post.id,
                "title" :post.writer,
                "content" :post.content,
                "category" :post.category,
                "create" :post.created_at
            }
            post_json_all.append(post_json)
        
        return JsonResponse({
            'status' :200,
            'message': "최근 게시글 목록 조회 성공",
            'data' : post_json_all
        },json_dumps_params={'ensure_ascii': False})


def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello lielion-12th!"
        })
    
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def detail(request,pk):  #html 로 코멘트 다는것 보여주는 함수 (admin 에서 확인됨. html은 미완)
    posts=Post.object.get(pk=pk)
    comment_form=CommentForm()
    context={
        'posts':posts,
        'comments':posts.comment_set.all(), 
        'comment_form':comment_form,
    }
    return render(request, 'posts/detail.html',context)


#  def comment_create(request,pk): #댓글을 작성하는 함수
#     posts=Post.object.get(pk=pk)
#     comment_form=CommentForm(request.POST)
#     if comment_form.is_valid():
#         comment=comment_form.save(commit=False)
#         comment.posts=posts
#         comment.save();
#     return redirect('post_detail',posts.pk)