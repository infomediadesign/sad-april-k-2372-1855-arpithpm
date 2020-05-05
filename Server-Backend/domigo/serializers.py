from datetime import timedelta
import datetime
from rest_framework import serializers
from .models import *
from rest_framework.response import Response


class PlanFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanFeature
        fields = "__all__"


class PlanSerializer(serializers.ModelSerializer):
    featuresobj = PlanFeatureSerializer(source="features", many=True, read_only=True)

    class Meta:
        model = Plan
        fields = "__all__"


class PetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PetCategory
        fields = "__all__"


class BreedSerializer(serializers.ModelSerializer):
    category = PetCategorySerializer(source="pet_category", read_only=True)
    plan = PlanSerializer(source="price_plan", read_only=True)

    class Meta:
        model = Breed
        fields = "__all__"


class UserPetsSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    breedobj = BreedSerializer(source="breed", read_only=True)

    def validate_owner(self, value):
        user = None
        request = self.context.get("request")
        if request:
            user = request.user
        if user != value:
            raise serializers.ValidationError(
                "Error: UserId mismatch. Userid field and the requested user doesn't match.")
        return value

    class Meta:
        model = UserPets
        fields = "__all__"


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


class PastBookingSerializer(serializers.ModelSerializer):
    """This serializer is used for the view to get past bookings."""
    """Problem with SerializerMethodField. Hence, new booking and past bookings are separate api"""
    total_price = serializers.SerializerMethodField()
    petobj = UserPetsSerializer(source="userpet", read_only=True)
    paymentobj = PaymentMethodSerializer(source="paymentmethod", read_only=True)
    paymentdone = serializers.SerializerMethodField()

    def get_paymentdone(self, obj):
        try:
            inst = PaymentReceived.objects.get(booking=obj)
        except:
            return False
        else:
            return True

    def get_total_price(self, obj):
        inst = obj.amount
        return inst

    class Meta:
        model = UserBooking
        exclude = ["booked_by"]


class NewBookingSerializer(serializers.ModelSerializer):
    booked_by = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def save(self, **kwargs):
        userpet = self.validated_data["userpet"]
        check_in_date = self.validated_data["check_in_date"]
        check_out_date = self.validated_data["check_out_date"]
        delta = check_out_date - check_in_date
        paymentmethod = self.validated_data["paymentmethod"]
        userpet = self.validated_data["userpet"]

        plan = userpet.breed.price_plan
        price = plan.price
        total_price = price * delta.days
        inst = UserBooking.objects.create(**self.validated_data, amount=total_price)

        for i in range(delta.days):
            temp_date = check_in_date + timedelta(days=i)
            try:
                BookingRegister.objects.create(date=temp_date, userbooking=inst, plan=plan, total_price=total_price,
                                               userpet=userpet)
            except:
                inst.delete()
                raise ValueError("Booking already exists during this period for this pet.")
        return {"message": "Success"}

    def validate(self, data):
        if data['check_in_date'] >= data['check_out_date']:
            raise serializers.ValidationError("Checkin date must be less than Checkout date.")
        check_in_date = data['check_in_date']
        check_out_date = data['check_out_date']
        delta = check_out_date - check_in_date
        plan = data['userpet'].breed.price_plan
        capacity = plan.capacity
        errors = []
        for i in range(delta.days):
            temp_date = check_in_date + timedelta(days=i)
            no_of_bookings = BookingRegister.objects.filter(date=temp_date, plan=plan).count()
            if no_of_bookings >= capacity:
                errors.append(str(temp_date))
        if errors:
            err_days = ", ".join(errors)
            raise serializers.ValidationError("Bookings are at full-capacity for " + err_days + ".")
        return data

    def validate_check_in_date(self, value):
        if value >= datetime.date.today():
            return value
        else:
            raise serializers.ValidationError(
                "Checkin date should be today or later.")

    def validate_check_out_date(self, value):
        if value >= datetime.date.today():
            return value
        else:
            raise serializers.ValidationError(
                "Checkin out should be today or later.")

    def validate_userpet(self, value):
        request_pet = value
        user = self.context.get("request").user
        userpetsids = list(user.pets.all().values_list('id', flat=True))
        if value.id in userpetsids:
            return value
        else:
            raise serializers.ValidationError(
                "Pet does not belong to requested user.")

    def validate_booked_by(self, value):
        user = None
        request = self.context.get("request")
        if request:
            user = request.user
        if user != value:
            raise serializers.ValidationError(
                "Error: UserId mismatch. 'booked_by' field and the requested user doesn't match.")
        return value

    class Meta:
        model = UserBooking
        fields = "__all__"


# Used for View of Receive Payments Table for the Frontend.
class UserBookingsListSerializer(serializers.ModelSerializer):
    booking_number = serializers.SerializerMethodField()
    person_name = serializers.SerializerMethodField()
    pet = serializers.SerializerMethodField()
    payment_done = serializers.SerializerMethodField()

    def get_booking_number(self, obj):
        return obj.id

    def get_person_name(self, obj):
        return obj.booked_by.first_name.title()

    def get_pet(self, obj):
        try:
            pet_name = obj.userpet.name.title()
        except:
            return "No Detail"
        else:
            return pet_name

    def get_payment_done(self, obj):
        try:
            payment_status = obj.paymentreceived
        except:
            return False
        else:
            return True

    class Meta:
        model = UserBooking
        exclude = ["paymentmethod", "booked_by", "userpet", "id"]


class PaymentReceivedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReceived
        fields = ["booking"]
