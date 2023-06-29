from .views import *
from django.urls import path

urlpatterns=[
    path('create-checkout-session/<pk>/',CreateCheckoutSessionView.as_view(),name="create-checkout-session"),
    path('',ProductLandingPageView.as_view(),name="landing-page"),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),
]
