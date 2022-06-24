from pydoc import Doc
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from main.models import Hospital,Doctor
from .forms import UserForm,DoctorForm,HospitalForm
from django import forms
from .choices import Department, States


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

    if request.method=="POST":
        hospitalform=HospitalForm(request.POST,request.FILES)

        username=request.POST['Username']
        password=request.POST['psw']
        confirmPassword=request.POST['cpsw']
        email=request.POST['Email']
        hospitalReg=request.POST.get('HospitalRegistrationNumber', '123')
      


        

        print(username,password,email,hospitalReg)

        usernameerror=""
        emailerror=""
        regerror=""
        passworderror=""
        
        # checking if the username already exists
        if User.objects.filter(username=username).exists():
            usernameerror="email id already exists"
        else:
            usernameerror=""
        
        #checking if the email already exists
        if User.objects.filter(email=email).exists():
            emailerror="Email already exists"
        else:
            emailerror=""
        
        # checking hospital registration number already exists
        print("before")
        if Hospital.objects.filter(HospitalRegisterationNumber=hospitalReg).exists():
            regerror="Hospital with the registraiton number already exists"
        else:
            regerror=""
        
        if password!=confirmPassword:
             passworderror="Passwords not matching"
        else:
            passworderror=""
        
        print("after")

        context={
            "form":HospitalForm,
            "usernameerror":usernameerror,
            " emailerror":emailerror,
            " regerror": regerror,
            " passworderror":passworderror
        } 


        if usernameerror!="" or emailerror!="" or regerror!="" or passworderror!="":
            return render(request,'Hospitalregistion.html',context)
        

        if hospitalform.is_valid():
            user=User.objects.create_user(username=username,password=password,email=email)
            user.save()

            hospitalform.save()

            return HttpResponse("Hospital registered") 






    if request.method=="GET":
        hospitalform=HospitalForm()
        context={'form':hospitalform}
        return render(request,'Hospitalregistion.html',context)

def doctorRegistration(request):

    if request.method=="POST":
        # creating an instance of the Doctor registration form
        doctorForm=DoctorForm(request.POST,request.FILES)

        #print(doctorForm)

        username=request.POST['Username']
        password=request.POST['psw']
        email=request.POST['Email']
        print(username,password,email)

        emailerror=""
        usernameerror=""

        if User.objects.filter(username=username).exists():
            usernameerror = "Username already exists"
        else:
            usernameerror = ""

        if User.objects.filter(email=email).exists():
            emailerror="email already exists"
        else:
            emailerror=""

        context={
            "form":DoctorForm,
            "emailerror":emailerror,
            "usernameerror":usernameerror
        }

        # if there is an error
        if usernameerror!="" or emailerror!="":
            print("in")
            return render(request,'doctor_regestration.html',context)
        
        if doctorForm.is_valid():
            print(username)
            user=User.objects.create_user(username=username,password=password,email=email)
            user.save()

            doctorForm.save()
            return HttpResponse("Registered")




    else:
        form=DoctorForm()
        context={'form':form}

        return render(request,'doctor_regestration.html',context)
    




# VIEWS FOR PROFILES

def doctorProfile(request,doctor_id):

    # doctor instance
    doctor=Doctor.objects.get(pk=doctor_id)
    print(doctor)

    
    # ratings instance
    count=doctor.Ratings_count

    if count!=0:
        five_starPercentage=100/100*count   # (number of 5 stars)
        four_starPercentage=100/100*count   # (number of 5 stars)
        three_starPercentage=100/100*count   # (number of 5 stars)
        two_starPercentage=100/100*count   # (number of 5 stars)
        one_starPercentage=100/100*count   # (number of 5 stars)
    else:
        five_starPercentage=100/100*count   # (number of 5 stars)
        four_starPercentage=100/100*count   # (number of 5 stars)
        three_starPercentage=100/100*count   # (number of 5 stars)
        two_starPercentage=100/100*count   # (number of 5 stars)
        one_starPercentage=100/100*count   # (number of 5 stars)
    
    ratings_percentage={
        "five_star":five_starPercentage,
        "five_star":four_starPercentage,
        "five_star":three_starPercentage,
        "five_star":two_starPercentage,
        "five_star":one_starPercentage
    }

    # doctor department
    dept=Department[doctor.Department-1][1]


    # doctor experience
    
    if doctor.YearsOfExperience==0:
        exp="Experience of the doctor not given"
    else:
        exp=doctor.YearsOfExperience

    context={
        'doctor':doctor,
        "ratings_percentage":ratings_percentage,
        "department":dept,
        'experience':exp
    }


    return render(request,'DoctorProfile.html',context)

   