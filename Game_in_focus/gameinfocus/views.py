from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm


def main(request):
    if request.method == "POST":
        return HttpResponse("main.html")
    else:
        userform = UserForm()
        return render(request, "main.html", {"form": userform})


def account(request):
    return HttpResponse('аккаунт')


def league_of_legends(request):
    return HttpResponse('Страница лиги легенд')


def site_settings(request):
    return HttpResponse('Настройки')

