from django.shortcuts import render
from rest_framework import viewsets
from .models import UserProfile, User
from .serializers import UserProfileSerializer
from rest_framework.response import Response

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def update(self, request, pk = None):
        print("hehe!!!!")
        user_profile = UserProfile.objects.get(pk = pk)
        print(user_profile)
        print(request.data)
        serializer = UserProfileSerializer(user_profile)
        user_profile = UserProfileSerializer.update(serializer, validated_data = request.data)
        super().update(request, pk)

    def partial_update(self, request, pk = None):
        print("hoho!!!")
        super().partial_update(request, pk)
