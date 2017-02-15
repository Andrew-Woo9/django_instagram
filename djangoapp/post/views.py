from django.http import HttpResponse
from django.shortcuts import render, redirect

from post.models import Post, Comment
from .form import PostForm

"""
post_list를 보여주는 화면을 구성
1. view에 post_list함수 작성
2. Tempalste에 post_lsit.html을 작성
3. View에서 post_list.html을 render하는 결과를 리턴하도록함
4. instagram/urls.py에 post/usrls.py를 연결 시킴 (app_name은 post)
5. '/post/'로 접속했을 때 post_list View에 연결되도록 post/urls.py에 내용을 구성
6. 전체 post를 가져오는 쿼리셋을 context로 넘기도록 post_list 뷰에 구현
7. post_list.hltml에서 {% for %}태그를 사용해  post_list의 내용을 순회하며 표현
"""


def post_list(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        comment_add(request, post_id=post_id)

    else:
        post = Post.objects.all()

        context = {
            'post_list': post
        }
        return render(request, 'post/post_list.html', context)

    return redirect('post:post')


def comment_add(request, post_id):
    if request.method == 'POST':

        form = PostForm(data=request.POST)

        if form.is_valid():
            user = request.user
            content = request.POST['content']
            post = Post.objects.get(id=post_id)

            Comment.objects.create(
                author=user,
                post=post,
                content=content,
            )
        else:
            return HttpResponse('Form invalid {}'.format(form.errors))

        return redirect('post:post_detail', post_id=post_id)
    else:
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request, 'post/post-detail.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)

    form = PostForm()

    context = {
        'post_detail': post,
        'form': form,
    }
    return render(request, 'post/post-detail.html', context)
