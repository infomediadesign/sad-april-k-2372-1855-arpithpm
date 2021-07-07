from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Plan(models.Model):
    """The model for the Pricing Plan"""
    name = models.CharField(max_length=200, null=False, blank=False, help_text="Give a name to the plan",
                            unique=True)
    created_date = models.DateField(auto_now=True)
    active = models.BooleanField(help_text="Make a plan active or inactive")
    price = models.FloatField(default=0.0, blank=False, null=False)
    capacity = models.IntegerField(default=1, blank=False, null=False)
    features = models.ManyToManyField('PlanFeature', related_name="features")

    def __str__(self):
        return self.name + " | " + str(self.active) + " | " + "₹ " + str(self.price) + " | capacity: " + str(
            self.capacity)


class PlanFeature(models.Model):
    """Feature for the Plan"""
    name = models.CharField(max_length=300, null=False, blank=False, help_text="Feature Name/Description")
    active = models.BooleanField(help_text="Active/Inactive")
    description = models.CharField(max_length=500, blank=True, null=True, help_text="Feature Name/Description")
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name + " | " + str(self.active)


class PetCategory(models.Model):
    """model for the category of the pet."""
    name = models.CharField(max_length=300, null=False, blank=False, help_text="Feature Name/Description")
    active = models.BooleanField(help_text="Active/Inactive")
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name + " | " + str(self.active)


class Breed(models.Model):
    pet_category = models.ForeignKey(PetCategory, on_delete=models.CASCADE, related_name="breeds")
    price_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=False, blank=False, help_text="Feature Name/Description")
    active = models.BooleanField(help_text="Active/Inactive")
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.pet_category) + " | " + str(self.price_plan) + " | " + self.name + " | " + str(self.active)

    class Meta:
        unique_together = [["pet_category", "name"]]


class UserPets(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, help_text="Name")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pets")
    date_of_birth = models.DateField(null=False, blank=False)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, null=False, blank=True,
                                   help_text="Write something about your pet.")
    instructions = models.CharField(max_length=300, null=False, blank=False,
                                    help_text="Write any special instructions to your pet handler.")

    def __str__(self):
        return self.name + " | owner: " + str(self.owner) + " | Breed: " + str(self.breed)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, help_text="Name")
    active = models.BooleanField(help_text="Active/Inactive")
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name + " | Status: " + str(self.active)


class UserBooking(models.Model):

    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="bookings")
    userpet = models.ForeignKey(UserPets, on_delete=models.SET_NULL, null=True)
    check_in_date = models.DateField(null=False, blank=False)
    check_out_date = models.DateField(null=False, blank=False)
    booked_on_date = models.DateField(auto_now=True)
    amount = models.FloatField(null=False, blank=False, default=0.0)
    paymentmethod = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return " id:" + str(self.id) + "| Booked by: " + str(self.booked_by) + " checkin date: " + str(
            self.check_in_date) + " checkout date: " + str(self.check_out_date)

    class Meta:
        unique_together = [["booked_by", "userpet", "check_in_date", "check_out_date"]]


status = (
    ("PAID", "PAID"),
    ("PENDING", "PENDING")
)


class PaymentReceived(models.Model):
    booking = models.OneToOneField(UserBooking, unique=True, on_delete=models.SET_NULL, null=True, related_name="paymentreceived")
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    received_date = models.DateField(auto_now=True)
    amount_received = models.FloatField(blank=False, null=False, default=0.0)

    def __str__(self):
        return "Booking#: " + str(self.booking.id) + " | Amount Received: " + str(self.amount_received)


class BookingRegister(models.Model):
    date = models.DateField(blank=False, null=False)
    userbooking = models.ForeignKey(UserBooking, on_delete=models.SET_NULL, null=True, related_name="register_entries")
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    userpet = models.ForeignKey(UserPets, on_delete=models.SET_NULL, null=True)
    total_price = models.FloatField(null=False, blank=False, default=0.0)

    class Meta:
        unique_together = [["date", "userpet"]]

    def __str__(self):
        return str(self.date) + " | userbooking: " + str(self.userbooking) + " | plan: " + str(
            self.plan) + " | price: " + str(self.total_price)
