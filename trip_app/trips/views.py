from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.utils import str_to_geopoint
from trips.models import Trip, TripRequest
from trips.permissions import IsTripDriverOrAdmin
from trips.serializers import TripSerializer, TripRequestSerializer


class TripViewSet(ModelViewSet):
    serializer_class = TripSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            self.permission_classes = [IsTripDriverOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Trip.objects.all()
        query_params = self.request.query_params

        time1 = query_params.get("time1")
        time2 = query_params.get("time2")
        start_point = query_params.get("sp")
        dest_point = query_params.get("dp")

        if time1 and time2:
            queryset = queryset.filter(dep_time__gt=time1, dep_time__lt=time2)

        if start_point and dest_point:
            start_point = str_to_geopoint(start_point)
            dest_point = str_to_geopoint(dest_point)
            # Annotate queryset with 2 attributes:
            # dist1 - distance between user and trip start point;
            # dist2 - between user and trip end point.
            # Order the queryset in the ascending order by sum distance,
            queryset = (
                queryset.annotate(dist1=Distance("start_point", start_point))
                .annotate(dist2=Distance("dest_point", dest_point))
                .order_by(F("dist1") + F("dist2"))
            )

        return queryset

    @action(detail=True, methods=["post"])
    def reserve(self, request, pk=None):
        """ Reserve a trip by sending a POST to api/trip/<trip_id>/reserve/."""
        trip = self.get_object()
        user = request.user
        if user == trip.driver:
            return Response(
                data="Driver can't be a passenger at the same time",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if trip.free_seats:
            if trip.man_approve:
                trip_request = TripRequest.objects.create(trip=trip, user=user)
                serializer = TripRequestSerializer(trip_request)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            trip.passengers.add(user)
            serializer = self.get_serializer(trip)
            return Response(serializer.data)
        return Response(
            data="There are no empty seats in this trip",
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True, methods=["get"], permission_classes=[IsTripDriverOrAdmin]
    )
    def requests(self, *args, **kwargs):
        """ The list of the requests related to the specific trip.
            GET /api/trips/<trip_id>/requests/. """
        trip = self.get_object()
        serializer = TripRequestSerializer(trip.requests, many=True)
        return Response(serializer.data)
