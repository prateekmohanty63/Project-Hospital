
from datetime import datetime
from django.db import models
from PIL import Image
from .choices import States,Department


# # Create your models here.

class User(models.Model):
    FirstName = models.CharField(max_length=150)
    LastName = models.CharField(max_length=150)
    Username = models.CharField(max_length=150)
    Email = models.CharField(max_length=150)
    DateOfBirth = models.CharField(max_length=150)
    MobileNumber = models.CharField(max_length=10)
    def __str__(self):
        return self.Username


class Doctor(models.Model):
    FirstName = models.CharField(max_length=150)  # doctor first name 
    LastName = models.CharField(max_length=150)   # doctor last name
    Email = models.CharField(max_length=150)      # doctor email 
    Username = models.CharField(max_length=150)   # doctor username
    DateOfBirth = models.CharField(max_length=150)
    ProfilePhoto = models.FileField(upload_to="DoctorPhotos/", default="DefaultPhotos/boy_avatar.jpg") # doctor profile photo 
    MobileNumber = models.CharField(max_length=13, default="Not available")                                   # doctor phone number 
    DoctorLicense = models.FileField(upload_to="DoctorDocuments/")                   # doctor License which is taken by goverment 
    YearsOfExperience = models.IntegerField(default=0)                              # Experience year 
    Rating = models.DecimalField(max_digits=2, decimal_places = 1, default=0.0)      # doctor rating 
    Ratings_stars = models.CharField(max_length=5,default="", blank= True)  
    non_stars = models.CharField(max_length=5,default="12345")
    Ratings_count = models.IntegerField(default=0) 
    Education = models.CharField(max_length=250, default="Not available")                         #  education  details 
    Masters = models.CharField(max_length=250, default="Not available")
    HospitalName = models.CharField(max_length=50)
    HospitalRegisterationNumber = models.CharField(max_length=100)                   # hospital name and all details
    City = models.CharField(max_length=100)
    State = models.IntegerField(choices=States, default=1)
    Pincode = models.CharField(max_length=20)
    Department = models.IntegerField(choices=Department, default=1)
    Description = models.CharField(max_length=150, default="Dear, be strong because your life will be better now. Time does not remain same. You will get well soon!")
    Achievements1 = models.CharField(max_length=50, default="No achievements added recently")
    Achievements2 = models.CharField(max_length=50, default="No achievements added recently")
    Achievements3 = models.CharField(max_length=50, default="No achievements added recently")
    Achievements4 = models.CharField(max_length=50, default="No achievements added recently")
    def __str__(self):
        return self.Username
    # image resize function 
    def save(self):
        super().save()  # saving image first

        img = Image.open(self.ProfilePhoto.path) # Open image using self

        if img.height > 350 or img.width > 350:
            new_img = (350, 350)
            img.thumbnail(new_img)
            img.save(self.ProfilePhoto.path)
    


class Hospital(models.Model):
    HospitalName = models.CharField(max_length=150)   # Hospital Name  
    HospitalRegisterationNumber = models.CharField(max_length=150)  # Hospital Registeration 
    HospitalLicense = models.FileField(upload_to="HospitalDocuments/")
    HospitalPhoto = models.FileField(upload_to="HospitalPhotos/", default="DefaultPhotos/hospitalPhotos.jpg") #hospital photo
    Email = models.CharField(max_length=150)
    Username = models.CharField(max_length=150)
    HospitalEshtablishDate = models.DateField()     # Eshtablish Date 
    HospitalDescription = models.TextField(max_length=250, default="Dear, be strong because your life will be better now. Time does not remain same. You will get well soon!")
    Rating = models.DecimalField(max_digits=2, decimal_places = 1, default=0.0)
    Ratings_stars = models.CharField(max_length=5,default="", blank=True)
    non_stars = models.CharField(max_length=5,default="12345")
    Ratings_count = models.IntegerField(default=0)  
    Town = models.CharField(max_length=150)
    City = models.CharField(max_length=150)
    Pincode = models.CharField(max_length=150)
    State = models.IntegerField(choices=States, default=1)
    ChiefMedicalOfficer = models.CharField(max_length=150)
    ChiefMedicalOfficerCertificate = models.FileField(upload_to="ChiefDoctorDocuments/")
    ChiefMedicalOfficerPhoto = models.FileField(upload_to="ChiefDoctorPhotos/", default="DefaultPhotos/doctt.png")
    CheifMedicalOfficerDescription = models.CharField(max_length=250, default="Dear, be strong because your life will be better now. Time does not remain same. You will get well soon!")
    PhoneNumber = models.CharField(max_length=20)
    Achievements1 = models.CharField(max_length=50, default="No Hospital information added recently")
    Achievements2 = models.CharField(max_length=50, default="No Hospital information added recently")
    Achievements3 = models.CharField(max_length=50, default="No Hospital information added recently")
    Achievements4 = models.CharField(max_length=50, default="No Hospital information added recently")
    Achievements5 = models.CharField(max_length=50, default="No Hospital information added recently")
    Achievements6 = models.CharField(max_length=50, default="No Hospital information added recently")
    def __str__(self):
        return self.HospitalName




# Doctor review
class DocReview(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.DO_NOTHING)
    star_rating=models.TextField(blank=True)
    non_rating=models.TextField(blank=True)
    review=models.TextField(blank=True)
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    review_date=models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.user.Username
        
