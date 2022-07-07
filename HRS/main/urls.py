from unicodedata import name
from .import views
from unicodedata import name
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('',views.index,name='index'),
    path('signin/',views.signIn,name='signin'),
    path('signout/',views.signout,name='signout'),
    path('signup/',views.signUp,name='signup'),
    path('userReg/',views.userRegistration,name='userReg'),
    path('hospitalReg/',views.hospitalRegistration,name='hospitalReg'),
    path('doctorReg/',views.doctorRegistration,name='doctorReg'),

    # profile views

    path('doctorProfile/<int:doctor_id>',views.doctorProfile,name='doctorProfile'),

    # doctor review
    path('doctorReview/',views.docReview,name='doctorReview'),

    
    # profile update
    path('docProUpdate/',views.DocProfileUpdate,name='DocProfileUpdate'),

    # search views
    path('DocsearchResult/',views.DocsearchResult,name='DocsearchResult'),

    # doctor appointment
    path('docAppointment/',views.DoctorAppointment,name='docAppointment'),
]