

class Slot:
    def __init__(self, owner, position) -> None:
        self.player = owner
        self.slot_id = position
        self.card = None
        self._state = None

    def set_card(self, card):
        self.card = card

    def remove_card(self):
        self.card = None

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
    
