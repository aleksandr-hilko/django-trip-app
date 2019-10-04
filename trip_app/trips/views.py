from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Trip
from .serializers import TripSerializer


# Create your views here.
class CreateTripView(CreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)


# Create your views here.
class ListTripView(ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['price']

    # def get_queryset(self):
    #     qs = Trip.objects.all()
