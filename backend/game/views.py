from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Game
from .serializers import GameSerializer 
from rest_framework.response import Response
from user_auth.permissions import GameViewSetPermissions 
# Create your views here.


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer 
    permission_classes = [GameViewSetPermissions]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, pk = None):
        print("hoho!!!")
        return super().partial_update(request, pk)

    def retrieve(self, request, pk = None):
        print(request.user)
        return super().retrieve(request, pk)

    @action(detail = True, methods = ['get'])
    def list_games(self, request, *args, **kwargs):
        print("Listing Available games !!!!")
        return super().list(request, *args, **kwargs)

    @action(detail = True, methods = ['get'])
    def create_game(self, request, *args, **kwargs):
        print("Creating game !!!!")
        return None

