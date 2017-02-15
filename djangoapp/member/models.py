from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class MyUser(PermissionsMixin, AbstractBaseUser):
    CHOICE_GENDER = (
        ('m', 'Mail'),
        ('f', 'Female'),
    )
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=1, choices=CHOICE_GENDER)
    nickname = models.CharField(max_length=20)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def get_full_name(self):
        return '{} ({})'.format(
            self.nickname,
            self.username,
        )

    def get_short_name(self):
        return self.username
