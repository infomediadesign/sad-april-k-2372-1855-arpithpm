from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(
    [Plan, PlanFeature, PetCategory, Breed, UserPets, PaymentMethod, UserBooking, BookingRegister, PaymentReceived])
