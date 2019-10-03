from rest_framework.generics import ListCreateAPIView

from .models import Trip
from .serializers import TripSerializer


# Create your views here.
class ListCreateTrip(ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)
