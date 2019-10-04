from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from core.utils import str_to_geopoint
from .models import Trip
from .serializers import TripSerializer


class TripListCreateApiView(ListCreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ['price']

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

    def get_queryset(self):
        queryset = Trip.objects.all()
        query_params = self.request.query_params

        time1 = query_params.get("time1")
        time2 = query_params.get("time2")
        sp = query_params.get("sp")
        dp = query_params.get("dp")

        if time1 and time2:
            queryset = queryset.filter(dep_time__gt=time1, dep_time__lt=time2)

        if sp and dp:
            sp = str_to_geopoint(sp)
            dp = str_to_geopoint(dp)

            queryset = queryset.annotate(dist1=Distance('start_point', sp))
            queryset = queryset.annotate(dist2=Distance('dest_point', dp))
            queryset = queryset.annotate(sum_distance=F('dist1') + F('dist2'))
            queryset = queryset.order_by('sum_distance')

        return queryset
