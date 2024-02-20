from django.shortcuts import render
from django.http import HttpResponse


def main(request):
    return HttpResponse('hello')


def account(request):
    return HttpResponse('аккаунт')


def league_of_legends(request):
    return HttpResponse('Страница лиги легенд')


def site_settings(request):
    return HttpResponse('Настройки')

