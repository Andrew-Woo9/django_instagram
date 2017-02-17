from django.conf import settings
from django.db import models

from post.models.post import Post

__all__ = (
    'Comment',
)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return 'post[{}]\'s Comment[{}]'.format(
            self.post_id,
            self.id,
            self.author_id,
        )
