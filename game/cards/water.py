from game.cards import BaseCard, SpellMixin
from game.actions import *
from game.buff import BaseBuff
from game.slot import Slot

class BaseWaterCard(BaseCard):
    type = "Water"

class Meditation(SpellMixin, BaseWaterCard):
    name = "Meditation"
    spell = True
    mana_cost = 1

    def summon_actions(self, *args, **kwargs):
        for element in ["fire", "air", "earth"]:
            yield ManaIncrease(doer = self, target = self.player, element = element, increase = 1, *args, **kwargs)

class SeaSprite(BaseWaterCard):
    name = "Sea Sprite"
    mana_cost = 2
    attack = 5
    life = 22

    def start_of_owner_turn_actions(self, *args, **kwargs):
        yield SpecialAttack(doer = self, target = self.slot.player, damage = 2, stage = "start of owner turn", *args, **kwargs)

class MerfolkApostate(BaseWaterCard):
    name = "Merfolk Apostate"
    mana_cost = 3
    attack = 3
    life = 10

    def summon_actions(self, *args, **kwargs):
        yield ManaIncrease(doer = self, target = self.slot.player, element = "fire", increase = 2, *args, **kwargs)
    
class IceGolem(BaseWaterCard):
    name = "Ice Golem"
    mana_cost = 4
    attack = 4
    life = 12

    def take_damage(self, damage, type, stage, *args, **kwargs):
        if type != "BasicAttack":
            return None
        return super().take_damage(damage, type, stage, *args, **kwargs)

class MerfolkElder(BaseWaterCard):
    name = "Merfolk Elder"
    mana_cost = 5
    attack = 3
    life = 16

    def summon_actions(self, *args, **kwargs):

        def buff_function(target):
            mana_inc = target.get_mana_inc("air")
            target.set_mana_inc("air", mana_inc + 1)
        
        def debuff_function(target):
            mana_inc = target.get_mana_inc("air")
            target.set_mana_inc("air", mana_inc - 1)
        
        buff = BaseBuff(self, self.slot.player, buff_function, debuff_function, *args, **kwargs)
        self.buffs = [buff]
        
        yield ApplyBuff(buff = buff, doer = self, target = self.slot.player, stage = "summon", *args, **kwargs)

class IceGuard(BaseWaterCard):
    name = "Ice Guard"
    mana_cost = 6
    attack = 3
    life = 20

    