from rest_framework import generics
from .serializers import CreateNewUserSerializer


class ContactCreateAPI(generics.CreateAPIView):
    serializer_class = CreateNewUserSerializer
