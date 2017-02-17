from django.http import HttpResponse
from django.shortcuts import render, redirect

from post.form import CommentForm
from post.models import Post, Comment

__all__ = (
    'comment_delete',
    'comment_add',
)


def comment_delete(request, post_id, comment_id):
    """
    1. post_detail.html 의  Comment 표현 loop 내부에 form을 생성
    2. 요청 view(url)가 comment_delete가 되도록 함
    3. 요청을 받은 후 적절히 삭제처리
    4. redirect
    """
    if request.method == 'POST':
        commnet = Comment.objects.get(id=comment_id)
        if commnet.author.id == request.user.id:
            commnet.delete()

        return redirect('post:post')


def comment_add(request, post_id):
    if request.method == 'POST':

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            user = request.user
            content = comment_form.cleaned_data['content']
            post = Post.objects.get(id=post_id)
            # post.add_comment(user, content)
            Comment.objects.create(
                author=user,
                post=post,
                content=content,
            )
        else:
            return HttpResponse('Form invalid {}'.format(comment_form.errors))

        return redirect('post:post')
    else:
        comment_form = CommentForm()
        context = {
            'comment_form': comment_form,
        }
        return render(request, 'post/post-detail.html', context)
