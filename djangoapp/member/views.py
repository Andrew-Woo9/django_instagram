from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect

from .forms import LoginForm, SignupForm


def login(request):
    # post로 전달되었을 때
    if request.method == 'POST':

        form = LoginForm(data=request.POST)
        if form.is_valid():
            # html 파일에서 POST요청을 보내기 위해서 폼2개를 정의하고 버튼을 생성
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            # user가 존재할 경우
            if user is not None:
                auth_login(request, user)
                return redirect('post:post')
                # return render(request, 'member/logout.html')
            # user가 존재하지 않을 경우
            else:
                form.add_error(None, 'ID or PW 실패')
                # return HttpResponse('failed')

    # Get으로 전달되었을 때
    else:
        form = LoginForm()

    context = {
        'form': form,
    }
    return render(request, 'member/login.html', context)


def logout(requset):
    auth_logout(requset)
    return redirect('member:login')


def profile(request):
    context = {

    }
    return render(request, 'member/profile.html', context)


def signup(request):
    """
    회원가입을 구현하세요
    1. member/signup.html파일 생성
    2. Signup Form 클래스 구현
    3. 해당 Form을 사용해서 signup.html 템플릿 구성
    4. POST요청을 받아 MyUser객체를 생성 후 로그인
    5. 로그인 완료되면 post_list뷰로 이동
    """

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.create_user()
            login(request, user)

            return redirect('post:post')

    else:
        form = SignupForm()

    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)
