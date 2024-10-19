from rest_framework import routers
from .views import GameViewSet


router = routers.DefaultRouter()
router.register(r"games", GameViewSet, basename = "games")

