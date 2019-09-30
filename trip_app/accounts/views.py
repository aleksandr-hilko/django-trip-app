from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .serializers import UserSerializer

User = get_user_model()


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
