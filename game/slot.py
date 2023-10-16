
class Slot:
    def __init__(self, owner, position) -> None:
        self.player = owner
        self.slot_id = position
        self.card = None
        self._state = None
        self.buffs_doer = set()
        self.buffs_target = set()

    def set_card(self, card):
        self.card = card
        for buff in self.buffs_target:
            buff.apply_buff(target = self.card)

    def remove_card(self):
        card = self.card
        self.card = None
        return card

    @property
    def is_empty(self):
        if self.card is None:
            return True
        return False
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def set_state(self, value):
        self._state = value

    def take_damage(self, damage, *args, **kwargs):
        if self.card is None:
            self.player.take_damage(damage, *args, **kwargs)
        else:
            self.card.take_damage(damage, *args, **kwargs)
    
    def get_healed(self, health, *args, **kwargs):
        if self.card is not None:
            self.card.get_healed(health)

    def get_neighbours(self):
        if self.slot_id == "A":
            return [self.player.slots["B"]]
        elif self.slot_id == "B":
            return [self.player.slots["A"], self.player.slots["C"]]
        elif self.slot_id == "C":
            return [self.player.slots["B"], self.player.slots["D"]]
        elif self.slot_id == "D":
            return [self.player.slots["C"], self.player.slots["E"]]
        elif self.slot_id == "E":
            return [self.player.slots["D"], self.player.slots["F"]]
        elif self.slot_id == "F":
            return [self.player.slots["E"]]

    
