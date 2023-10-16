from game.cards import BaseCard, SpellMixin
from game.actions import *
from game.buff import BaseBuff, managed_by_buff
from game.slot import Slot

class BaseWaterCard(BaseCard):
    type = "water"

class Meditation(SpellMixin, BaseWaterCard):
    name = "Meditation"
    spell = True
    _mana_cost = 1

    def summon_actions(self, *args, **kwargs):
        for element in ["fire", "air", "earth"]:
            yield ManaIncrease(doer = self, target = self.player, element = element, increase = 1, *args, **kwargs)

class SeaSprite(BaseWaterCard):
    name = "Sea Sprite"
    _mana_cost = 2
    _attack = 5
    _life = 22

    def start_of_owner_turn_actions(self, *args, **kwargs):
        yield SpecialAttack(doer = self, target = self.slot.player, damage = 2, stage = "start of owner turn", *args, **kwargs)

class MerfolkApostate(BaseWaterCard):
    name = "Merfolk Apostate"
    _mana_cost = 3
    _attack = 3
    _life = 10

    def summon_actions(self, *args, **kwargs):
        yield ManaIncrease(doer = self, target = self.slot.player, element = "fire", increase = 2, *args, **kwargs)
    
class IceGolem(BaseWaterCard):
    name = "Ice Golem"
    _mana_cost = 4
    _attack = 4
    _life = 12

    def take_damage(self, damage, type, stage, *args, **kwargs):
        if type != "BasicAttack":
            return None
        return super().take_damage(damage, type, stage, *args, **kwargs)

class MerfolkElder(BaseWaterCard):
    name = "Merfolk Elder"
    _mana_cost = 5
    _attack = 3
    _life = 16

    def summon_actions(self, *args, **kwargs):

        def f(func):
                def _func(_obj, element, *args, **kwargs):
                    _output = func(_obj, element, *args, **kwargs)
                    if element == "air":
                        _output += 1
                    return _output
                return _func
       
        def buff_function(target):
            target.get_mana_inc.apply_buff(f)
        
        def debuff_function(target):
            target.get_mana_inc.remove_buff(f)
        
        buff = BaseBuff(self, self.slot.player, buff_function, debuff_function, *args, **kwargs)
        self.buffs = [buff]
        
        yield ApplyBuff(buff = buff, doer = self, target = self.slot.player, stage = "summon", *args, **kwargs)

class IceGuard(BaseWaterCard):
    name = "Ice Guard"
    _mana_cost = 6
    _attack = 3
    _life = 20

    def summon_actions(self, *args, **kwargs):
        
        def f(func):
                def _func(_obj, damage, *args, **kwargs):

                    _output = func(_obj, damage//2, *args, **kwargs)
                    
                    return _output
                return _func
       
        def buff_function(target):
            target.take_damage.apply_buff(f)
        
        def debuff_function(target):
            target.take_damage.remove_buff(f)

        
        buff = BaseBuff(self, self.slot.player, buff_function, debuff_function, *args, **kwargs)
        self.buffs = [buff]
        
        yield ApplyBuff(buff = buff, doer = self, target = self.slot.player, stage = "summon", *args, **kwargs)

class GiantTurtle(BaseWaterCard):
    name = "Giant Turtle"
    _mana_cost = 7 
    _attack = 5
    _life = 16

    def take_damage(self, damage, type, stage, *args, **kwargs):
        return super().take_damage(max(damage - 5, 0), type, stage, *args, **kwargs)
    
class AcidicRain(SpellMixin, BaseWaterCard):
    name = "Acidic Rain"
    spell = True
    _mana_cost = 8

    def summon_actions(self, *args, **kwargs):
        owner = self.player
        opponent = self.player.opponent

        for slot_id, slot in owner.slots.items():
            if slot.card is not None:
                yield SpecialAttack(doer = self, target = slot.card, damage = 15, stage = "summon", *args, **kwargs)
        
        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                yield SpecialAttack(doer = self, target = slot.card, damage = 15, stage = "summon", *args, **kwargs)
        
        for element in opponent.mana:
            yield ManaDrain(doer = self, target = opponent, element = element, decrease = 1, *args, **kwargs)

class MerfolkOverlord(BaseWaterCard):

    name = "Merfolk Overlord"
    _mana_cost = 9
    _attack = 7
    _life = 35

    def summon_actions(self, *args, **kwargs):

        def f(func):
                def _func(_obj, *args, **kwargs):
                    _output = func(_obj, *args, **kwargs)
                    _output.extend(_obj.turn_actions(*args, **kwargs))
                    return _output
                return _func
       
        def buff_function(target):
            if isinstance(target, BaseCard):
                target.summon_actions.apply_buff(f)
        
        def debuff_function(target):
            if isinstance(target, BaseCard):
                target.summon_actions.remove_buff(f)

        
        for neighbour in self.slot.get_neighbours():
            buff = BaseBuff(self, neighbour, buff_function, debuff_function, *args, **kwargs)
            self.buffs_doer.append(buff)
            
            yield ApplyBuff(buff = buff, doer = self, target = neighbour, stage = "summon", *args, **kwargs)

class WaterElemental(BaseWaterCard):

    name = "Water Elemental"
    _mana_cost = 10
    _life = 37

    @managed_by_buff
    @property
    def attack(self):
        return self.slot.player.get_mana(self.type)
    
    def summon_actions(self, *args, **kwargs):

        yield Heal(health = 10, doer = self, target = self.slot.player, *args, **kwargs)

      
        def f(func):
                def _func(_obj, element, *args, **kwargs):
                    _output = func(_obj, element, *args, **kwargs)
                    if element == self.type:
                        _output += 1
                    return _output
                return _func
       
        def buff_function(target):
            target.get_mana_inc.apply_buff(f)
        
        def debuff_function(target):
            target.get_mana_inc.remove_buff(f)
        
        
        buff = BaseBuff(self, self.slot.player, buff_function, debuff_function, *args, **kwargs)
        self.buffs = [buff]
        
        yield ApplyBuff(buff = buff, doer = self, target = self.slot.player, stage = "summon", *args, **kwargs)
    


class MindMaster(BaseWaterCard):

    name = "Mind Master"
    _mana_cost = 11
    _attack = 6
    _life = 23
    buffs = list()

    def summon_actions(self, *args, **kwargs):

        def f(func):
                def _func(_obj, element, *args, **kwargs):
                    _output = func(_obj, element, *args, **kwargs)
                    _output += 1
                    return _output
                return _func
          
       
        def buff_function(target):
            if isinstance(target, BaseCard):
                target.get_mana_inc.apply_buff(f)
        
        def debuff_function(target):
            if isinstance(target, BaseCard):
                target.get_mana_inc.remove_buff(f)

        
        buff = BaseBuff(self, self.slot.player, buff_function, debuff_function, *args, **kwargs)
        self.buffs.append(buff)
        
        yield ApplyBuff(buff = buff, doer = self, target = self.slot.player, stage = "summon", *args, **kwargs)


class AstralGuard(BaseWaterCard):

    name = "Astral Guard"
    _mana_cost = 12
    _attack = 1
    _life = 18
    buffs = list()

    def summon_actions(self, *args, **kwargs):

        def f(func):
                def _func(_obj, element, *args, **kwargs):
                    _output = func(_obj, element, *args, **kwargs)
                    _output -= 1
                    return _output
                return _func
          
       
        def buff_function(target):
            if isinstance(target, BaseCard):
                target.get_mana_inc.apply_buff(f)
        
        def debuff_function(target):
            if isinstance(target, BaseCard):
                target.get_mana_inc.remove_buff(f)

        
        buff = BaseBuff(self, self.slot.player.opponent, buff_function, debuff_function, *args, **kwargs)
        self.buffs.append(buff)
        
        yield ApplyBuff(buff = buff, doer = self, target = self.slot.player.opponent, stage = "summon", *args, **kwargs)