
from pydoc import Doc
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from main.models import Hospital,Doctor,DocReview
from .forms import DoctorForm,HospitalForm
from django import forms
from .choices import Department, States
from django.contrib import auth


# Create your views here.


def index(request):
    return render(request,'index.html')

def signIn(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        
        # based on returned value user get logged .
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Signed in successfully")
            return redirect('index')
        else:
            return render(request, 'signin_fail.html')

    else:
        return render(request, 'signin.html')

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
            return redirect('userRegistration')
            


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

    # fetching all the reviews of the doctor , ordered by latest date
    queryset_list=DocReview.objects.order_by('-review_date').filter(doctor=doctor)

    five_stars = 0
    for review  in queryset_list:
        if review.star_rating == "12345":
            five_stars = five_stars + 1
    four_stars = 0
    for review  in queryset_list:
        if review.star_rating == "1234":
            four_stars = four_stars + 1
    three_stars = 0
    for review  in queryset_list:
        if review.star_rating == "123":
            three_stars = three_stars + 1
    two_stars = 0
    for review  in queryset_list:
        if review.star_rating == "12":
            two_stars = two_stars + 1
    one_stars = 0
    for review  in queryset_list:
        if review.star_rating == "1":
            one_stars = one_stars + 1

    
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

    
    rating_count={
        "five_star":five_stars,
        "four_star":four_stars,
        "three_star":three_stars,
        "two_star":two_stars,
        "one_star":one_stars
    }
    
    ratings_percentage={
        "five_star":five_starPercentage,
        "five_star":four_starPercentage,
        "five_star":three_starPercentage,
        "five_star":two_starPercentage,
        "five_star":one_starPercentage
    }

    # doctor department
    dept=Department[doctor.Department-1][1]

    # fetching the doctor review (taking only 3)
    queryset_list=DocReview.objects.order_by('-review_date').filter(doctor=doctor)[:3]
    flag=0

    if request.POST=="POST":
        flag=1
        queryset_list=DocReview.objects.order_by('-review_date').filter(doctor=doctor)[:3]


    # doctor experience
    
    if doctor.YearsOfExperience==0:
        exp="Experience of the doctor not given"
    else:
        exp=doctor.YearsOfExperience

    context={
        'doctor':doctor,
        'doctor_reviews':queryset_list,
        'flag':flag,
        'ratings_count':rating_count,
        "ratings_percentage":ratings_percentage,
        "department":dept,
        'experience':exp
    }


    return render(request,'DoctorProfile.html',context)




# Doctor review

def docReview(request):

    if request.method=="POST":
        doctor_id=request.POST['doctor_id']
        doctor_name=request.POST['doctor_name']

       # print(doctor_id)
        #print(doctor_name)

        # check if the user is signed in 
        if not request.user.is_authenticated:
            return redirect('signin')
        
        try:
            username=request.POST['username']
            star_rating=request.POST['rating']
        except:
            return redirect('/doctorProfile/'+doctor_id)
        non_rating=""

        if star_rating=='1':
            non_rating="2345"
        elif star_rating == '12':
            non_rating = "345"
        elif star_rating == '123':
            non_rating = "45"
        elif star_rating == '1234':
            non_rating = "5"
        elif star_rating == '12345':
            non_rating = ""
        
        review=request.POST['review']

        # check if the user is registered for not
        # print("username")
        # print(request.user.username)
        # user=User.objects.all().filter(Username=request.user.username).get()
    
        try:
            user=User.objects.all().filter(username=request.user.username).get()
            
        except: 
            messages.error(request,"Please register for posting review")
            return redirect('/doctorProfile/'+doctor_id)
        
        doctor=Doctor.objects.all().filter(Username=doctor_name).get()

        # adding review to the database

        # print('printing user')
        # print(user)

        reviewed=DocReview(doctor=doctor,user=user,star_rating=star_rating,non_rating=non_rating,review=review)
       # print(reviewed) 

        # save to database
        reviewed.save()

        # calculating the average rating

        queryset_list=DocReview.objects.order_by('-review_date').filter(doctor=doctor)

        avg=[]
        length=0


        for doctor in queryset_list:
            length=length+1
            avg.append(len(doctor.star_rating))

        avg=sum(avg)/len(avg)

        stars=""

        if avg > 4.5:
            stars = "12345"
            non_stars = ""
        elif avg > 3.5:
            stars = "1234"
            non_stars = "1"
        elif avg > 2.5:
            stars = "123"
            non_stars = "12"
        elif avg > 1.5:
            stars = "12"
            non_stars = "123"
        elif avg > 0.5:
            stars = "1"
            non_stars = "1234"

        
        # updating the doctor reviews in the doctor model

        doctor=Doctor.objects.all().filter(Username=doctor_name).update(Rating=avg,Ratings_stars=stars,Ratings_count=length,non_stars=non_stars)
        messages.success(request,"Added review successfully")
        return redirect('/doctorProfile/'+doctor_id)



        return HttpResponse("Review Posted")
    



   