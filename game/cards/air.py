from game.cards import BaseCard, SpellMixin, CardMap
from game.actions import *
from game.buff import BaseBuff, managed_by_buff
from game.slot import Slot

class BaseAirCard(BaseCard):
    type = "air"

class FaerieApprentice(BaseAirCard):
    name = "Faerie Apprentice"
    _mana_cost = 1
    _attack = 4
    _life = 12

    def summon_actions(self, *args, **kwargs):

        def f(func):
                def _func(_obj, card_name, slot_id, *args, **kwargs):
                    _output = func(_obj, card_name, slot_id, *args, **kwargs)
                    for summon_action  in _output:
                        if summon_action.doer.spell:
                            summon_action.damage += 1
                    return _output
                return _func
       
        def buff_function(target):
            target.play_card.apply_buff(f)
        
        def debuff_function(target):
            target.play_card.remove_buff(f)
        
        buff = BaseBuff(self, self.slot.player, buff_function, debuff_function, *args, **kwargs)
        self.buffs = [buff]
        
        yield ApplyBuff(buff = buff, doer = self, target = self.slot.player, stage = "summon", *args, **kwargs)

class Griffin(BaseAirCard):
    name = "Griffin"
    _mana_cost = 2
    _attack = 3
    _life = 15

    def summon_actions(self, *args, **kwargs):
        if self.slot.player.get_mana(self, self.type, *args, **kwargs) >=3:
            yield SpecialAttack(damage = 5, doer = self, target = self.slot.player.opponent, stage = "summon", *args, **kwargs)
        else:
            return []
        
class CallToThunder(SpellMixin, BaseAirCard):
    name = "Call To Thunder"
    _mana_cost = 3
    spell = True

    def summon_actions(self, target, *args, **kwargs):
        yield SpecialAttack(damage = 6, doer = self, target = target, stage = "summon", *args, **kwargs)
        yield SpecialAttack(damage = 6, doer = self, target = self.player.opponent, stage = "summon", *args, **kwargs)

class FaerieSage(BaseAirCard):
    name = "Faerie Sage"
    _mana_cost = 4
    _attack = 4
    _life = 19

    def summon_actions(self, *args, **kwargs):
        earth_power = self.slot.player.get_mana("earth")
        yield Heal(doer = self, target = self.slot.player, health = min(earth_power, 10), *args, **kwargs)

class WallOfLightning(BaseAirCard):
    name = "Wall of Lightning"
    _mana_cost = 5
    _attack = 0
    _life = 28
    wall = True

    def start_of_owner_turn_actions(self, *args, **kwargs):
        yield SpecialAttack(doer = self, target = self.slot.player, damage = 4, stage = "start of owner turn", *args, **kwargs)

class LightningBolt(SpellMixin, BaseAirCard):
    name = "Lightning Bolt"
    _mana_cost = 6
    spell = True

    def summon_actions(self, *args, **kwargs):
        yield SpecialAttack(damage = 5 + self.player.get_mana("air"), doer = self, target = self.player.opponent, stage = "summon", *args, **kwargs)

class Phoenix(BaseAirCard):
    name = "Phoenix"
    _mana_cost = 7
    _attack = 7
    _life = 16

    def death_actions(self, *args, **kwargs):
        super().death_actions(self, *args, **kwargs)
        if self.slot.player.get_mana("fire") >= 10:
            self.slot.set_card(CardMap.get_card_by_name( player = self.slot.player, slot = self.slot, slot_id = self.slot.slot_id))

class ChainLightning(SpellMixin, BaseAirCard):
    name = "Chain Lightning"
    _mana_cost = 8
    spell = True

    def summon_actions(self, *args, **kwargs):
        yield SpecialAttack(doer = self, target = self.player.opponent, damage = 9, stage = "summon", *args, **kwargs)
        for slot_id, slot in self.player.opponent.slots.items():
            if slot.card is not None:
                yield SpecialAttack(doer = self, target = slot.card, damage = 9, stage = "summon", *args, **kwargs)

class LightningCloud(BaseAirCard):
    name = "Lightning Cloud"
    _mana_cost = 9
    _attack = 4
    _life = 20

    def turn_actions(self, *args, **kwargs):
        opponent = self.slot.player.opponent
        yield BasicAttack(damage = self.attack, doer = self, target = opponent, *args, **kwargs)
        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                yield BasicAttack(damage = self.attack, doer = self, target = slot, *args, **kwargs)

class Tornado(SpellMixin, BaseAirCard):
    name = "Tornado"
    _mana_cost = 10
    spell = True

    def summon_actions(self, slot_id, *args, **kwargs):
        yield RemoveCard(doer = self, target = self.player.opponent, slot_id = slot_id, stage = "summon", *args, **kwargs)
    
class AirElemental(BaseAirCard):

    name = "Air Elemental"
    _mana_cost = 11
    _life = 44

    @managed_by_buff
    @property
    def attack(self):
        return self.slot.player.get_mana(self.type)
    
    def summon_actions(self, *args, **kwargs):

        yield SpecialAttack(damage = 8, doer = self, target = self.slot.player.opponent, stage ="summon", *args, **kwargs)

      
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
 
class Titan(BaseAirCard):
    name = "Titan"
    _mana_cost = 12
    _attack = 9
    _life = 40

    def summon_actions(self, *args, **kwargs):
        opposing_slot = self.slot.player.opponent.slots[self.slot.slot_id]
        if opposing_slot.card is not None:
            yield SpecialAttack(doer = self, target = opposing_slot, damage =15, stage = "summon", *args, **kwargs)
        else:
            return []
