from slot import Slot



class BaseGameConfig:

    @classmethod
    def configure_player(cls, player):
        cls.set_player_mana(player)
        cls.set_player_mana_inc(player)

    @staticmethod
    def set_player_mana(player):
        player.set_mana("fire", 5)
        player.set_mana("water", 5)
        player.set_mana("air", 4)
        player.set_mana("earth", 5)
        player.set_mana(player.special, 2)
    
    @staticmethod
    def set_player_mana_inc(player):
        player.set_mana_inc("fire", 1)
        player.set_mana_inc("water", 1)
        player.set_mana_inc("air", 1)
        player.set_mana_inc("earth", 1)
        player.set_mana_inc(player.special, 1)
    
    @staticmethod
    def set_player_slots(player):
        player.slots = [Slot(player, "A"), Slot(player, "B"), Slot(player, "C"), Slot(player, "D"), Slot(player, "E"), Slot(player, "F")]


class BaseGame:
    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.turn = [self.player_1, 1]
        self.is_ended = False

    def switch_turn(self):
        if self.turn[0] == self.player_1:
            self.turn[0] = self.player_2
        else:
            self.turn[0] = self.player_1
            self.turn[1] += 1

