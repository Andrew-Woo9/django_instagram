from django.db import models

from member.models import MyUser


class Post(models.Model):
    author = models.ForeignKey(MyUser)
    photo = models.ImageField(upload_to='post', blank=True)
    # like_users =
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


class Comment(models.Model):
    author = models.ForeignKey(MyUser)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return 'post[{}]\'s Comment[{}]'.format(
            self.post_id,
            self.id,
            self.author_id,
        )


class Postlike(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
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
