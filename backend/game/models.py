from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):

    class Meta:

        db_table = "game"

    game_state = [
        ("open", "Open"),
        ("active", "Active"),
        ("ended", "Ended")
    ]

    game_id = models.UUIDField(primary_key = True)
    status = models.CharField(choices = game_state, max_length = 20)
    player_1 = models.ForeignKey(to = User, on_delete = models.CASCADE, related_name="%(class)s_player_1")
    player_2 = models.ForeignKey(to = User, on_delete = models.CASCADE, related_name="%(class)s_player_2")
