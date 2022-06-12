from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request,'index.html')

def signin(request):
    return render(request,'signin.html')

def signup(request):
    return render(request,'signup.html')