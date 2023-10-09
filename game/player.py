from cards import CardMap
from cards import Deck

special_mapping = {
    "Death": "death",
    "Chaos": "chaos"
}

class BasePlayer:
    element_list = ["fire", "water", "air", "earth"]

    def __init__(self, name, special, *args, **kwargs) -> None:
        self.name = name
        self.special = special
        self.element_list.append(special_mapping.get(special))
        self.mana = {}
        self.mana_inc = {}
        self._life = 0
        self.deck = Deck()

    def build_by_config(self, game_config, *args, **kwargs):
        game_config.configure_player(self)

    @property
    def life(self):
        return self._life
    
    @life.setter
    def life(self, value):
        self._life = value

    def set_mana(self, element, value = None, *args, **kwargs):
        if value == None:
            value = self.mana.get(element, 0) + self.mana_inc.get(element, 0)
        self.mana[element] = value

    def decrease_mana(self, element, value = 0, *args, **kwargs):
        self.mana[element] -= value

    def set_mana_inc(self, element, value = 1, *args, **kwargs):
        self.mana_inc[element] = value

    def take_damage(self, damage, *args, **kwargs):
        self.life -= damage
    
    def get_healed(self, health, *args, **kwargs):
        self.life += health

    def mana_drain(self, element, decrease, *args, **kwargs):
        self.mana[element] -= decrease

    def mana_increase(self, element, increase, *args, **kwargs):
        self.mana[element] += increase
    
    def shuffle_deck(self, element, *args, **kwargs):
        self.deck.shuffle(element)

    def play_card(self, card_name, slot_id, *args, **kwargs):
        card_info = CardMap.get_card_info(card_name)
        if self.slots[slot_id].is_empty:
            if self.mana.get(card_info.get("type"))>=card_info.get("mana_cost"):
                self.slots[slot_id].set_card(CardMap.get_card_by_name(card_name, player = self, slot = self.slots[slot_id], slot_id = slot_id))
                self.decrease_mana(card_info.get("type"), card_info.get("mana_cost", 0))
        


