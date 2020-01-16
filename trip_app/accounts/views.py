from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from accounts.permissions import IsAuthOwnerOrAdminOnly
from core.models import User
from .serializers import UserSerializer


class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthOwnerOrAdminOnly]


class CurrentUserAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
