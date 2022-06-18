from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserForm
from django import forms


# Create your views here.


def index(request):
    return render(request,'index.html')

def signIn(request):
    return render(request,'signin.html')

def signUp(request):
    return render(request,'signup.html')

def userRegistration(request):

    if request.method=="POST":
       # userform = UserForm(request.POST, request.FILES)
        print("POST")
        firstName=request.POST['fname']
        lastName=request.POST['lname']
        email=request.POST['email']
        dateOfBirth=request.POST['date']
        userName=request.POST['user_name']
        password1=request.POST['password1']
        password2=request.POST['password2']
        mobileNo=request.POST['mobileNumber']

        print(password1)
        print(password2)

        if password1==password2:
            print("in")
            if User.objects.filter(username=userName).exists():
                messages.info(request,'username taken')
                return redirect('userReg')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email is taken')
                return redirect('userReg')
            else:
                
                print('form is valid')
                user = User.objects.create_user(username=userName, password=password1, email=email)
                    #user.is_active = False
                user.save()
            # Save the Data to the Database  
                   # userform.save()
                return HttpResponse("REGISTERED")

                
                HttpResponse('Registered')
        
        else:
            messages.info(request,"Password not matching")
            return redirect('register')
            


        print(firstName)
        return HttpResponse("HELLO");


    if request.method=="GET":
        print("GET")
        return render(request,"user_registration.html")
    

def hospitalRegistration(request):
    return render(request,'Hospitalregistion.html')

def doctorRegistration(request):
    return render(request,'doctor_regestration.html')