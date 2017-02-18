from django import forms
from django.contrib.auth.password_validation import validate_password

from member.models import MyUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=MyUser.CHOICE_GENDER, widget=forms.RadioSelect)
    nickname = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=30, required=False)

    # 중복가입 방지
    def clean_username(self):
        username = self.cleaned_data['username']
        if MyUser.objects.filter(username=username):
            raise forms.ValidationError('username exists')

        return username

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        # 8자리이상 패스워드를 입력해야 합니다
        validate_password(password1)

        if password1 != password2:
            raise forms.ValidationError('패스워드 입력 맞나요')

        return password2

    def create_user(self):
        username = self.cleaned_data['username']
        password2 = self.cleaned_data['password2']
        email = self.cleaned_data['email']
        gender = self.cleaned_data['gender']
        nickname = self.cleaned_data['nickname']

        user = MyUser.objects.create_user(
            username=username,
            password=password2,
        )
        user.email = email
        user.gender = gender
        user.nickname = nickname
        user.save()

        return user
