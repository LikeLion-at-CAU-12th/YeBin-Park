# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
from .forms import CommentForm
from .models import Post

# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello lielion-12th!"
        })
    
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def get_post_detail(request,id):
    post = get_object_or_404(Post, pk=id)
    post_detail_json = {
        "id" : post.id,
        "title" : post.title,
        "content" : post.content,
        "writer" : post.writer,
        "category" : post.category,
    }

    return JsonResponse({
        'status' : 200,
        'message' : '게시글 조회 성공',
        'data' : post_detail_json
    })

def detail(request,pk):
    posts=Post.object.get(pk=pk)
    comment_form=CommentForm()
    context={
        'posts':posts,
        'comments':posts.comment_set.all(), 
        'comment_form':comment_form,
    }
    return render(request, 'posts/detail.html',context)

def comment_create(request,pk): #댓글을 작성하는 함수
    posts=Post.object.get(pk=pk)
    comment_form=CommentForm(request.POST)
    if comment_form.is_valid():
        comment=comment_form.save(commit=False)
        comment.posts=posts
        comment.save()
    return redirect('posts:detail',posts.pk)