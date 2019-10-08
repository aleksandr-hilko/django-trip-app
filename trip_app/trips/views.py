from core.utils import str_to_geopoint
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Trip
from .permissions import IsTripDriverOrAdmin
from .serializers import TripSerializer


class TripViewSet(ModelViewSet):
    serializer_class = TripSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            permission_classes = [IsTripDriverOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Trip.objects.all()
        query_params = self.request.query_params

        time1 = query_params.get("time1")
        time2 = query_params.get("time2")
        sp = query_params.get("sp")
        dp = query_params.get("dp")

        if time1 and time2:
            # We are looking for trips that belong to time range between time1 and time2
            queryset = queryset.filter(dep_time__gt=time1, dep_time__lt=time2)

        if sp and dp:
            sp = str_to_geopoint(sp)
            dp = str_to_geopoint(dp)
            # Annotate queryset with 2 attributes (dist1 - distance between user start point and
            # start point of the trip; dist2 - between user destination point and destination point
            # of the trip. Order the queryset in the ascending order by sum distance, which means that user
            # should be able to see the closest trips first )
            queryset = queryset.annotate(dist1=Distance('start_point', sp)). \
                annotate(dist2=Distance('dest_point', dp)). \
                order_by(F('dist1') + F('dist2'))

        return queryset
