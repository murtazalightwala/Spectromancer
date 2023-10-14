from game.slot import Slot
from game.actions import ApplyDebuff, BasicAttack
from game.buff import BuffManager

class Deck:
    def __init__(self) -> None:
        pass
    
    def shuffle(self, element):
        pass

class BaseCard:
    type:str
    name:str
    _attack:int
    _life:int
    _mana_cost:int
    _state:str
    slot: Slot
    spell:bool = False
    wall:bool = False

    @BuffManager
    @property
    def attack(self):
        return self._attack

    @BuffManager
    @property
    def life(self):
        return self._life

    @BuffManager
    @property
    def mana_cost(self):
        return self._mana_cost

    @BuffManager
    @property
    def state(self):
        return self._state

    def __init__(self, slot, *args, **kwargs):
        self.slot = slot
        self.buffs_doer = set()
        self.buffs_target = set()
        self.state = "drafted"

    def take_damage(self, damage, type, stage, *args, **kwargs):
        self.life -= damage

    def get_healed(self, health, stage, *args, **kwargs):
        self.life += health

    def start_of_round_actions(self, *args, **kwargs):
        return []

    def start_of_owner_turn_actions(self, *args, **kwargs):
        return []
    
    def start_of_opponent_turn_actions(self, *args, **kwargs):
        return []

    def end_of_round_actions(self, *args, **kwargs):
        return []

    def end_of_owner_turn_actions(self, *args, **kwargs):
        return []
    
    def end_of_opponent_turn_actions(self, *args, **kwargs):
        return []

    def summon_actions(self, *args, **kwargs):
        return []

    def death_actions(self, *args, **kwargs):
        for buff in self.buffs:
            yield ApplyDebuff(buff = buff, doer = self, target = buff.target, *args, **kwargs)

    def turn_actions(self, *args, **kwargs):
        opponent = self.slot.player.opponent
        yield BasicAttack(damage = self.attack, doer = self, target = opponent.slots[self.slot.slot_id], *args, **kwargs)
    

class SpellMixin:
    attack = 0
    life = 0

    def __init__(self, player, *args, **kwargs) -> None:
        self.player = player