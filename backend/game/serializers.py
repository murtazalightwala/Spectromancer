from user_auth.serializers import UserProfileSerializer, UserSerializer, UserWithProfileSerializer
from rest_framework import serializers
from .models import Game



class GameSerializer(serializers.ModelSerializer):

    player_1 = UserWithProfileSerializer()
    player_2 = UserWithProfileSerializer()

    class Meta:

        model = Game
        fields = "__all__"


