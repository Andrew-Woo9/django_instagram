from django.shortcuts import render, redirect

from post.form import CommentForm, PostForm
from post.models import Post

__all__ = (
    'post_list',
    'post_detail',
    'post_delete',
    'post_like_toggle',
    'post_add',
)

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
        from post.views import comment_add
        comment_add(request, post_id=post_id)

    else:
        post = Post.visibles.all()
        # post = Post.objects.all()

        context = {
            'posts': post
        }
        return render(request, 'post/post_list.html', context)

    return redirect('post:post')


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_form = CommentForm()

    context = {
        'post_detail': post,
        'comment_form': comment_form,
    }
    return render(request, 'post/post-detail.html', context)


def post_add(request):
    def create_post_comment(file, comment_content):
        post = Post(author=request.user, photo=file)
        post.save()

        if comment_content != '':
            post.add_comment(user=request.user, content=comment_content)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('photo')
            comment_content = form.cleaned_data.get('content', '').strip()

            for file in files:
                create_post_comment(file, comment_content)

            return redirect('post:post')

    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'post/post-add.html', context)


def post_delete(request, post_id, db_delete=False):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        if post.author.id == request.user.id:

            if db_delete:
                post.delete()
            else:
                post.is_visible = False

            post.save()

        return redirect('post:post')


def post_like_toggle(request, post_id):
    if not request.user.is_authenticated:
        return redirect('post:post')
    else:
        if request.method == 'POST':
            post = Post.objects.get(id=post_id)
            post.toggle_like(user=request.user)
            return redirect('post:post')
