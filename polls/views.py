from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def menu(request):
    return HttpResponse(("우리 메뉴는 많아요"))

def order_coffee(request):
    return HttpResponse("커피 한잔 주세요.")