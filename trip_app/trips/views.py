from django.contrib.gis.db.models.functions import Distance
from django.db.models import F
from rest_framework import status

from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.utils import str_to_geopoint, geocode
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
        if self.action in ['update', 'destroy', 'partial_update', 'requests']:
            self.permission_classes = [IsTripDriverOrAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
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


@api_view(['post'])
@permission_classes([IsAuthenticated])
def approve_trip_request(request, **kwargs):
    """ Approve trip request via
       POST api/trips/<int:trip_pk>/requests/<int:request_pk>/approve/. """
    trip_pk, request_pk = kwargs.get("trip_pk"), kwargs.get("request_pk")
    trip = get_object_or_404(Trip, pk=trip_pk)
    _check_trip_request_permissions(request, trip)
    if trip.free_seats:
        trip_request = get_object_or_404(trip.requests, pk=request_pk)
        trip_request.status = TripRequest.APPROVED
        trip_request.save()
        trip.passengers.add(trip_request.user)
        serializer = TripRequestSerializer(trip_request)
        return Response(data=serializer.data)
    return Response(
        "You can't approve this request because you haven't got free seats",
        status=status.HTTP_400_BAD_REQUEST)


@api_view(['post'])
@permission_classes([IsAuthenticated])
def decline_trip_request(request, **kwargs):
    """ Decline trip request via
        POST api/trips/<int:trip_pk>/requests/<int:request_pk>/decline/. """
    trip_pk, request_pk = kwargs.get("trip_pk"), kwargs.get("request_pk")
    trip = get_object_or_404(Trip, pk=trip_pk)
    _check_trip_request_permissions(request, trip)
    trip_request = get_object_or_404(trip.requests, pk=request_pk)
    trip_request.status = TripRequest.DECLINED
    trip_request.save()
    serializer = TripRequestSerializer(trip_request)
    return Response(data=serializer.data)


def _check_trip_request_permissions(request, trip):
    if trip.driver != request.user or not request.user.is_staff:
        raise PermissionDenied(
            detail="Only a trip driver or an admin can edit the trip request")
