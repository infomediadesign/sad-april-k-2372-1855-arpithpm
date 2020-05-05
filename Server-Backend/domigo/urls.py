from rest_framework import renderers
from .views import *
from django.urls import path
from .models import *

urlpatterns = [
    path("plan/", PlanView.as_view()),
    path("planfeature/", PlanFeatureView.as_view()),
    path("petcategory/", PetCategoryView.as_view()),
    path("breedlist/", BreedListView.as_view()),
    path("userpets/", UserPetsListView.as_view()),
    path("userpets/<int:pk>/", UserPetsUpdateView.as_view()),
    path("paymentmethods/", PaymentMethodListView.as_view()),
    path("newbooking/", NewUserBookingView.as_view()),
    path("pastbookings/", PastBookingView.as_view()),

    # routes for admin users on the frontend of the app
    path("admin/userbookings/", AdminUserBookingsList.as_view()),
    # for receiving payments from the frontend by admins.
    path("admin/receive-payment/", AdminReceivePayment.as_view())

]
