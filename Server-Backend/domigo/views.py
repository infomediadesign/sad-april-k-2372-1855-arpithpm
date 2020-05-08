from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import *
from .serializers import *
from .models import *
from rest_framework.renderers import JSONRenderer


class PlanView(generics.ListAPIView):
    queryset = Plan.objects.filter(active=True)
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny, ]


class PlanFeatureView(generics.ListAPIView):
    queryset = PlanFeature.objects.filter(active=True)
    serializer_class = PlanFeatureSerializer
    permission_classes = [permissions.AllowAny, ]


class PetCategoryView(generics.ListAPIView):
    queryset = PetCategory.objects.filter(active=True)
    serializer_class = PetCategorySerializer
    permission_classes = [permissions.AllowAny, ]


class BreedListView(generics.ListAPIView):
    queryset = Breed.objects.filter(active=True)
    serializer_class = BreedSerializer
    permission_classes = [permissions.AllowAny, ]


class UserPetsListView(generics.ListCreateAPIView):
    """Returns the all the addresses of the user"""
    serializer_class = UserPetsSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return UserPets.objects.filter(owner=user)


class UserPetsUpdateView(generics.DestroyAPIView):
    serializer_class = UserPetsSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        return UserPets.objects.all()


class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.filter(active=True)
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.AllowAny, ]


class NewUserBookingView(generics.CreateAPIView):
    """Returns the all the addresses of the user"""
    serializer_class = NewBookingSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except:
            print("poiuytr")
            return Response(data={"message": "Booking already exists during this period for this pet."}, status=403)
        else:
            return Response(serializer.data, status=201)

    def perform_create(self, serializer):
        # serializer = NewBookingSerializer(data=request.data)
        try:
            serializer.save()
        except:
            raise ValueError("Booking already exists during this period for this pet.")


class PastBookingView(generics.ListAPIView):
    """Returns the all the addresses of the user"""
    serializer_class = PastBookingSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = self.request.user
        return UserBooking.objects.filter(booked_by=user)


# Used for Receive Payments Table for the Frontend.
class AdminUserBookingsList(generics.ListAPIView):
    queryset = UserBooking.objects.all()
    serializer_class = UserBookingsListSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminReceivePayment(generics.CreateAPIView):
    queryset = PaymentReceived.objects.all()
    serializer_class = PaymentReceivedSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        inst = PaymentReceivedSerializer(data=request.data)
        if inst.is_valid():
            amount = inst.validated_data["booking"].amount
            PaymentReceived.objects.create(booking=inst.validated_data["booking"], received_by=request.user,
                                           amount_received=amount)
            # resp = UserBookingsListSerializer(UserBooking.objects.all(), many=True)
            # if resp.is_valid(raise_exception=True):
            # json = JSONRenderer().render(resp.data)
            # return Response(data=resp.data, status=201, content_type="text/json")
            return Response(data={"message": "Success."}, status=201)
        else:
            return Response(data={"error": "Payment has already been received."}, status=403)
