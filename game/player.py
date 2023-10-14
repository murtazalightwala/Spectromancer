from .cards import CardMap
from .cards import Deck
from game.buff import BuffManager

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
        self._game = None
        self.buffs_doer = set()
        self.buffs_target = set()

    def build_by_config(self, game_config, *args, **kwargs):
        game_config.configure_player(self)

    @property
    def life(self):
        return self._life
    
    @life.setter
    def life(self, value):
        self._life = value

    def get_mana(self, element, *args, **kwargs):
        return self.mana.get(element, 0)

    def set_mana(self, element, value = None, *args, **kwargs):
        if value == None:
            value = self.mana.get(element, 0) + self.mana_inc.get(element, 0)
        self.mana[element] = value

    def decrease_mana(self, element, value = 0, *args, **kwargs):
        self.mana[element] -= value
    
    def increase_mana(self, element, value, *args, **kwargs):
        self.mana[element] += value
    
    @BuffManager
    def get_mana_inc(self, element, *args, **kwargs):
        return self.mana_inc.get(element, 0)

    def set_mana_inc(self, element, value = 1, *args, **kwargs):
        self.mana_inc[element] = value

    def take_damage(self, damage, *args, **kwargs):
        self.life -= damage
    
    def get_healed(self, health, *args, **kwargs):
        self.life += health

    def mana_drain(self, element, decrease, *args, **kwargs):
        self.mana[element] -= decrease

    def shuffle_deck(self, element, *args, **kwargs):
        self.deck.shuffle(element)

    def play_card(self, card_name, slot_id, *args, **kwargs):
        card_info = CardMap.get_card_info(card_name)
        summon_actions = []
        if self.slots[slot_id].is_empty:
            if self.mana.get(card_info.get("type"))>=card_info.get("mana_cost"):
                card = CardMap.get_card_by_name(card_name, player = self, slot = self.slots[slot_id], slot_id = slot_id)
                self.slots[slot_id].set_card(card)
                self.decrease_mana(card_info.get("type"), card_info.get("mana_cost", 0))
                summon_actions = [x for x in card.summon_actions()]
        return summon_actions
    
        
    
    @property
    def game(self):
        return self._game
    
    @game.setter
    def set_game(self, game):
        self._game = game

    @property
    def opponent(self):
        if self.game is None:
            return None
        if self.game.player_1 == self:
            return self.game.player_2
        else:
            return self.game.player_1
        
    def play_summon_effects(self, *args, **kwargs):
        pass
        
    

