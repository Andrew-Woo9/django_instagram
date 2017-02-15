from django.db import models, IntegrityError


class MyUser(models.Model):
    username = models.CharField('이름', max_length=10, primary_key=True)
    last_name = models.CharField('성', max_length=10)
    first_name = models.CharField('이름', max_length=10)
    nick_name = models.CharField('낙네임', max_length=20)
    email = models.EmailField('이메일', null=True, blank=True)
    date_joined = models.DateTimeField('가입일', auto_now_add=True)
    last_modified = models.DateField('마지막수정일', blank=True, null=True)
    following = models.ManyToManyField(
        'self',
        related_name='follower_set',
        symmetrical=False,
        blank=True,
    )

    def __str__(self):
        return self.username

    # 임의 값의 데이터를 넣어주기 위한 메소드
    @staticmethod
    def create_dummy_user(num):
        import random
        last_name_list = ['방', '이', '김', '정']
        first_name_list = ['영이', '철수', '수영', '지희']
        nick_name_list = ['물개', '이쁜이', '못난이', '진상']
        created_count = 0
        for i in range(num):
            try:
                MyUser.objects.create(
                    username='User{}'.format(i + 1),
                    last_name=random.choice(last_name_list),
                    first_name=random.choice(first_name_list),
                    nick_name=random.choice(nick_name_list),
                )
                created_count += 1
            except IntegrityError as e:
                print(e)

        return created_count

    @staticmethod
    def assign_global_variables():
        import sys
        module = sys.modules['__main__']

        # MyUser객체 중 'User'로 시작하는 객체들만 조회하여 users변수에 할당
        users = MyUser.objects.filter(username__startswith='user')

        # user를 순회하며
        for index, user in enumerate(users):
            # __main__모듈에 'u1,u2,u3 ...'이름으로 가가 MyUser객체를 할당
            setattr(module, 'u{}'.format(index + 1), user)

    def follow(self, user):
        self.following.add(user)

    def unfollow(self, user):
        self.following.remove(user)

    @property
    def follows(self):
        return self.followr_set.all()

    def change_nickname(self, new_nickname):
        self.nick_name = new_nickname
        self.save()
