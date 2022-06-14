from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request,'index.html')

def signIn(request):
    return render(request,'signin.html')

def signUp(request):
    return render(request,'signup.html')

def userRegistration(request):
    return render(request,"user_registration.html")