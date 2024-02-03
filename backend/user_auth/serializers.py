from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserProfile, User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        exclude = ["last_login", "is_superuser", "is_staff", "is_active", "date_joined", "user_permissions", "groups"]
        extra_kwargs = {'password': {'write_only': True}}


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
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
   
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.first_name + " " + user.last_name
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token
