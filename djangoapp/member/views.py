from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm


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
                return redirect('/admin')
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
    return HttpResponse('logout Success')
