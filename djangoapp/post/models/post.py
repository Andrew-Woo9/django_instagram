from django.conf import settings
from django.db import models

from member.models import MyUser
from post.models import Comment

__all__ = (
    'Post',
    'Postlike',
)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    photo = models.ImageField(upload_to='post', blank=True)
    content = models.TextField(max_length=300, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True)
    like_users = models.ManyToManyField(
        MyUser,
        through='PostLike',
        related_name='like_post_set'
    )

    def __str__(self):
        return 'Post{}'.format(self.id)

    class Meta:
        ordering = ('-id',)

    def toggle_like(self, user):
        # pl_list = Postlike.objects.filter(post=self, user=user)
        pl_list = self.postlike_set.filter(user=user)

        # 코드1 #############
        # if pl_list.exist():
        #     pl_list.delete()
        # else:
        #     Postlike.objects.create(post=self, user=user)
        #
        # 코드2 #############
        # if문 부터 else까지 한줄로 표현한 코드
        # pl_list.delete() if pl_list.exist() else Postlike.objects.create(post=self, user=user)

        return self.postlike_set.create(user=user) if not pl_list.exists() else pl_list.delete()

    def add_comment(self, user, content):
        Comment.object.create(
            user=user,
            content=content
        )

    @property
    def like_count(self, post, user):
        return self.like_users.count()

    @property
    def comment_count(self, post):
        return self.comment_set.count()


# USER 모델을 참조할때 settings.AUTH_USER_MODEL 로 사용
# settings 파일 안에 AUTH_USER_MODEL = 'member.MyUser' 이라고 정의하여 둠
class Postlike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True, null=True)

    class Meta:
        unique_together = (
            ('user', 'post'),
        )

    def __str__(self):
        return 'post[{}]\'s Like[{}]'.format(
            self.post_id,
            self.id,
            self.user_id,
        )
