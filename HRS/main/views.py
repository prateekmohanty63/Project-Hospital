
from collections import UserList
from os import stat_result
from pickle import NONE
from pydoc import Doc
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages

from main.models import Hospital,Doctor,DocReview,DocAppointment
from .forms import DoctorForm,HospitalForm
from django import forms
from .choices import Department, States
from django.contrib import auth
from django.core.files.storage import FileSystemStorage


# Create your views here.


def index(request):
    username=request.user.username


    # storing all the users, doctors and hospitals

    users=User.objects.all()
    doctors=Doctor.objects.all()
    hospitals=Hospital.objects.all()

    user_list=[]
    doctor_list=[]
    hospital_list=[]

    # username of user , doctors and hospitals in a list
    for user in users:
        user_list.append(user.username)
    
    for doctor in doctors:
        doctor_list.append(doctor.Username)

    for hospital in hospitals:
        hospital_list.append(hospital)

    
    USER=NONE
    type="default"

    if username in user_list:
        USER=User.objects.all().filter(username=username).get()
        type="user"
    
    if username in doctor_list:
        USER=Doctor.objects.all().filter(Username=username).get()
        type="doctor"
    
    if username in hospital_list:
        USER=Hospital.objects.all().filter(Username=username).get()
        type="hospital"

    context={
        'USER':USER,
        'type':type
    }

    return render(request,'index.html',context)

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

# this view is for the common page of signup
def signUp(request):
    return render(request,'signup.html')


# signout view

def signout(request):
    user=request.user
    context={
        'USER':user
    }
    auth.logout(request)
    messages.success(request,"Signed out successfully",context)
    return redirect('index')

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
    



# doctor profile updated

def DocProfileUpdate(request):
    if request.method=="POST":
        flag=0
        data=request.POST
        files=request.FILES.get('profilePhoto')
        fs=FileSystemStorage()

        try:
            fs.save("DoctorPhotos/"+files.name,files)
            Path="DoctorPhotos/"+str(files.name)
        except AttributeError:
            flag=1
        
        # fetching the doctor from the username
        doctor=Doctor.objects.all().filter(Username=request.user.username).get()

        if data['fname'] == "":
            fname = doctor.FirstName
        else:
            fname = data['fname']

        if data['lname'] == "":
            lname = doctor.LastName
        else:
            lname = data['lname']

        if flag == 0:
            profilePhoto = Path
        else:
            profilePhoto = doctor.ProfilePhoto

        if data['phn_no'] == "":
            mobilenum = doctor.MobileNumber
        else:
            mobilenum = data['phn_no']

        if data['yoe'] == "":
            yoe = doctor.YearsOfExperience
        else:
            yoe = data['yoe']

        if data['hospname'] == "":
            hospname = doctor.HospitalName
        else:
            hospname = data['hospname']

        if data['hospRegNum'] == "":
            hospRegNum = doctor.HospitalRegisterationNumber
        else:
            hospRegNum = data['hospRegNum']

        if data['city'] == "":
            city = doctor.City
        else:
            city = data['city']

        if data['state'] == '0':
            state = doctor.State
        else:
            state = data['state']
            

        if data['pinc'] == "":
            pincode = doctor.Pincode
        else:
            pincode = data['pinc']

        if data['dept'] == '0':
            dept = doctor.Department
        else:
            dept = data['dept']

        if data['desc'] == "":
            desc = doctor.Description
        else:
            desc = data['desc']

        if data['ach1'] == "":
            ach1 = doctor.Achievements1
        else:
            ach1 = data['ach1']

        if data['ach2'] == "":
            ach2 = doctor.Achievements2
        else:
            ach2 = data['ach2']

        if data['ach3'] == "":
            ach3 = doctor.Achievements3
        else:
            ach3 = data['ach3']

        if data['ach4'] == "":
            ach4 = doctor.Achievements4
        else:
            ach4 = data['ach4']

        
        doctorUpdated=Doctor.objects.all().filter(Username=request.user.username).update(
            FirstName = fname,
            LastName = lname,
            ProfilePhoto = profilePhoto,
            MobileNumber = mobilenum,
            YearsOfExperience = yoe ,          
            HospitalName = hospname,
            HospitalRegisterationNumber = hospRegNum,
            City = city,
            State = state,
            Pincode = pincode,
            Department = dept,
            Description = desc,
            Achievements1 = ach1,
            Achievements2 = ach2,
            Achievements3 = ach3,
            Achievements4 = ach4

        )

        doctor_id=str(doctor.id)
        messages.success(request,"Updated Profile successfully")
        return redirect('/doctorProfile/'+doctor_id)


    else:
        return render(request,'doctorUpdateProfile.html')
    



# search for doctor

def DocsearchResult(request):
    if request.method=="POST":
        # Fetching doctors based on the first name
        queryset_list=Doctor.objects.order_by('-FirstName')

        # taking states from choices
        State_result=States

        dept_result=Department
        
        # searching based on first name
        if 'first_name' in request.GET:

            Firstname=request.GET['first_name']

            if Firstname:
                queryset_list=queryset_list.filter(FirstName_iexact=Firstname)
        

        # searching based on last name

        if 'last_name' in request.GET:
            LastName=request.GET['last_name']

            if LastName:
                queryset_list=queryset_list.filter(LastName_iexact=LastName)

        
        # searching based on city

        if 'city' in request.GET:
            City=request.GET['city']

            if City:
                queryset_list=queryset_list.filter(City_iexact=City)
        
        if 'state' in request.GET:
        #if the searched option is not equal to All i.e. if User select any other state than All then we're storing the state in State variable and filtering the required State from database.
        #If user selects All then we dont filter any states and pass.
            if not request.GET['state'] == "29":
                State = request.GET['state']
                if State:
                    queryset_list = queryset_list.filter(State = State)
          
    #Department of doctor 
        if 'dept' in request.GET:
        #if the searched option is not equal to All i.e. if User selects any other department than All then we're storing the department in Departments variable and filtering the required Department from database.
        #If user selects All then we dont filter any Department and pass.
            if not request.GET['dept'] == "7":
             Departments = request.GET['dept']

            if Departments:
                    queryset_list = queryset_list.filter(Department = Departments)
   
    #pincode
    #Getting pincode from User Search for Doctor
        if 'pincode' in request.GET:
         #Storing pincode in Pincode
            Pincode = request.GET['pincode']
         #if Pincode exists then we are filtering the required pincode from database and storing it in queryset_list.
            if Pincode:
             queryset_list = queryset_list.filter(Pincode = Pincode)
        

        dict=[]

        for result in queryset_list:
            Result=result

            State_result=States[result.State-1][1]
            dept_result=Department[result.Department-1][1]

            res={
                'result':Result,
                'State_result':State_result,
                'dept_result':dept_result
            }

            dict.append(res)

        
        context={
            'dict':dict
        }
    
        return render(request,'searchbarResults.html',context)
   


# doctor appointment

def DoctorAppointment(request):

    if request.method=="POST":
        print("hello")
        DoctorUsername=request.POST['dname']
        DateOfAppointment=request.POST['date']
        additionalMessage=request.POST['message']


        # Checking weather the user is signed in or not
        if not request.user.is_authenticated:
            messages.error(request,"Please sign in ")
            return redirect('index')

        
        # retriving the user and doctor
        user = User.objects.all().filter(username=request.user.username).get()
        doctor=Doctor.objects.all().filter(Username=DoctorUsername).get()
        #print(user)

        # checking weather the doctor exists or not
        if not doctor:
            messages.error(request,'Doctor does not exists')
            return redirect('index')
        
        appointment=DocAppointment(user=user,doctor=doctor,dateOfAppointment=DateOfAppointment,AdditionalMessage=additionalMessage)
        appointment.save()

        # send a mail to doctor and the user

        messages.success(request,'Appointment sent successfully')
        return redirect('index')

