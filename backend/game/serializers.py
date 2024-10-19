from rest_framework import serializers
from .models import Game



class GameSerializer(serializers.Serializer):

    class Meta:

        model = Game
        fields = "__all__"
