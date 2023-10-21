from rest_framework import serializers
from .models import UserProfile, User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        exclude = ["last_login", "is_superuser", "is_staff", "is_active", "date_joined", "user_permissions", "groups"]


class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=True)

    class Meta: 
        model = UserProfile    
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data = user_data)
        user_profile = UserProfile.objects.create(user = user, **validated_data)
        return user_profile
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user")
        print(instance)
        user = UserSerializer.update(UserSerializer(), validated_data = user_data)
        user_profile = UserProfile.objects.update(user = user, **validated_data)
        return user_profile