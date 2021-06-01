from django.shortcuts import render,redirect,HttpResponse

def test(request):
    return HttpResponse("hi")