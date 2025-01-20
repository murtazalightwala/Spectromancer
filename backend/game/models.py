from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

class Game(models.Model):

    class Meta:

        db_table = "game"

    game_state = [
        ("open", "Open"),
        ("active", "Active"),
        ("ended", "Ended")
    ]

    game_id = models.UUIDField(primary_key = True, default = uuid4, editable = False)
    status = models.CharField(choices = game_state, max_length = 20)
    player_1 = models.ForeignKey(to = User, on_delete = models.CASCADE, related_name="%(class)s_player_1")
    player_2 = models.ForeignKey(to = User, on_delete = models.CASCADE, related_name="%(class)s_player_2", null = True, default = None, blank = True)

    def save(self, *args, **kwargs):
        if not self.pk:  # New object being created
            if self.player_1 is None:
                raise ValueError("Player 1 cannot be null.")
            self.status = "open"
        else:
            if self.player_1 == self.player_2:
                raise ValueError("Player 1 and Player 2 cannot be the same.")
            if self.status == "active" and player_2 is None:
                raise ValueError("Game cannot start with player_2 None.")
            old_game = Game.objects.filter(pk=self.pk).first()
            if old_game is not None:
                if old_game.status == "ended":
                    raise ValueError("Cannot change status of an ended game.")
                if self.status == "open" and old_game.status != "open":
                    raise ValueError("Cannot change status back to open.")
                if self.status == "active" and old_game.status != "open":
                    raise ValueError("Status can only be changed to active from open.")
                if self.status == "ended" and old_game.status != "active":
                    raise ValueError("Status can only be changed to ended from active.")
        return super().save(*args, **kwargs)
