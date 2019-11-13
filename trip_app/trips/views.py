from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.utils import str_to_geopoint, geocode
from trips.models import Trip, TripRequest
from trips.permissions import (
    IsTripDriverOrAdmin,
    IsRequestUserOrAdmin,
    IsRequestDriverOrAdmin,
)
from trips.serializers import TripSerializer, TripRequestSerializer


class TripViewSet(ModelViewSet):
    """ Provide default CRUD actions with custom 'reserve' and 'requests'
        actions. """

    serializer_class = TripSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def perform_create(self, serializer):
        """ Set driver for a Trip model before writing in DB. """
        serializer.save(driver=self.request.user)

    def get_permissions(self):
        """ Define permissions for associated views. """
        if self.action in ["update", "destroy", "partial_update", "requests"]:
            self.permission_classes = [IsTripDriverOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        """ Get the list of trips for this viewset
            and filter it depending on request query parameters. """
        queryset = Trip.objects.all()
        query_params = self.request.query_params

        time1 = query_params.get("time1")
        time2 = query_params.get("time2")

        if time1 and time2:
            queryset = queryset.filter(dep_time__gt=time1, dep_time__lt=time2)

        point1 = query_params.get("point1")
        point2 = query_params.get("point2")
        address1 = query_params.get("addr1")
        address2 = query_params.get("addr2")
        geo_coords = all([point1, point2])
        address_coords = all([address1, address2])
        if geo_coords or address_coords:
            # TODO: Consider possibility of using factory pattern here
            if geo_coords:
                geo_point1 = str_to_geopoint(point1)
                geo_point2 = str_to_geopoint(point2)
            elif address_coords:
                geo_point1 = geocode(address1)
                geo_point2 = geocode(address2)

            # Annotate queryset with 2 attributes:
            # dist1 - distance between user and trip start point;
            # dist2 - between user and trip end point.
            # Order the queryset in the ascending order by sum distance,
            queryset = (
                queryset.annotate(
                    dist1=Distance("start_point__point", geo_point1)
                )
                .annotate(dist2=Distance("dest_point__point", geo_point2))
                .order_by(F("dist1") + F("dist2"))
            )

        return queryset

    @action(detail=True, methods=["post"])
    def reserve(self, request, pk=None):
        """ Reserve a trip via POST api/trips/<trip_id>/reserve/. """
        trip = self.get_object()
        user = request.user
        if user == trip.driver:
            return Response(
                data="Driver can't be a passenger at the same time",
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.requests.filter(trip_id=pk).exists():
            return Response(
                data="You have already requested this trip",
                status=status.HTTP_400_BAD_REQUEST,
            )
        trip_request = trip.process_request(user)
        serializer = TripRequestSerializer(trip_request)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def requests(self, *args, **kwargs):
        """ The list of the requests related to the specific trip.
            GET /api/trips/<trip_id>/requests/. """
        trip = self.get_object()
        serializer = TripRequestSerializer(trip.requests, many=True)
        return Response(serializer.data)


class TripRequestViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """ Provide listing or retrieving trip requests,
        with the approve/decline/cancel trip request custom actions. """

    serializer_class = TripRequestSerializer
    queryset = TripRequest.objects.all()
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def get_permissions(self):
        if self.action in ["approve", "decline"]:
            self.permission_classes = [IsRequestDriverOrAdmin]
        elif self.action == "cancel":
            self.permission_classes = [IsRequestUserOrAdmin]
        elif self.action == "retrieve":
            self.permission_classes = [
                IsRequestUserOrAdmin | IsRequestDriverOrAdmin
            ]
        elif self.action == "list":
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    @action(detail=True, methods=["post"])
    def approve(self, *args, **kwargs):
        """ Approve trip request via
            POST api/trip-requests/<id>/approve/. """
        trip_request = self.get_object()
        trip_request.approve()
        serializer = TripRequestSerializer(trip_request)
        return Response(data=serializer.data)

    @action(detail=True, methods=["post"])
    def decline(self, *args, **kwargs):
        """ Approve trip request via
            POST api/trip-requests/<id>/decline/. """
        trip_request = self.get_object()
        trip_request.decline()
        serializer = self.serializer_class(trip_request)
        return Response(data=serializer.data)

    @action(detail=True, methods=["post"])
    def cancel(self, *args, **kwargs):
        """ Cancel reservation for a trip by sending a
            POST to api/trip_requests/<id>/cancel/. """
        trip_request = self.get_object()
        trip_request.cancel()
        serializer = self.serializer_class(trip_request)
        return Response(serializer.data)
