from game.cards import BaseCard, SpellMixin, CardMap
from game.actions import *
from game.buff import BaseBuff, managed_by_buff
from game.slot import Slot

class BaseEarthCard(BaseCard):
    type = "earth"


class ElvenHealer(BaseEarthCard):
    name = "Elven Healer"
    _mana_cost = 1
    _attack = 2
    _life = 12

    def start_of_owner_turn_actions(self, *args, **kwargs):
        yield Heal(doer = self, target = self.slot.player, health= 3, stage = "start of owner turn", *args, **kwargs)

class NaturesRitual(SpellMixin, BaseEarthCard):
    name = "Nature's Ritual"
    _mana_cost = 2
    spell = True

    def summon_actions(self, target, *args, **kwargs):
        yield Heal(doer = self, target = target, health = 8, stage = "summon", *args, **kwargs)
        yield Heal(doer = self, target = self.player, health = 8, stage = "summon", *args, **kwargs)

class ForestSprite(BaseEarthCard):
    name = "Forest Sprite"
    _mana_cost = 3
    _attack = 1
    _life = 22

    def turn_actions(self, *args, **kwargs):
        yield BasicAttack(doer = self, target = self.slot.player.opponent, damage = self.attack, stage = "turn", *args, **kwargs)
        for slot_id, slot in self.slot.player.opponent.slots.items():
            if slot.card is not None:
                yield BasicAttack(doer = self, target = slot.card, damage = self.attack, stage = "turn", *args, **kwargs)

class Rejuvenation(SpellMixin, BaseEarthCard):
    name = "Rejuvenation"
    _mana_cost = 4
    spell = True
    
    def summon_actions(self, *args, **kwargs):
        earth_power = self.player.get_mana("earth")
        yield Heal(doer = self, target = self.player, health = earth_power * 2, *args, **kwargs)

class ElfHermit(BaseEarthCard):
    name = "Elf Hermit"
    _mana_cost = 5
    _attack = 1
    _life = 13

    def summon_actions(self, *args, **kwargs):
        
        def f(func):
                def _func(_obj, element, *args, **kwargs):
                    _output = func(_obj, element, *args, **kwargs)
                    if element == self.type:
                        _output += 2
                    return _output
                return _func
       
        def buff_function(target):
            target.get_mana_inc.apply_buff(f)
        
        def debuff_function(target):
            target.get_mana_inc.remove_buff(f)
        
        buff = BaseBuff(self, self.slot.player, buff_function, debuff_function, *args, **kwargs)
        self.buffs = [buff]
        
        yield ApplyBuff(buff = buff, doer = self, target = self.slot.player, stage = "summon", *args, **kwargs)

class NaturesFury(SpellMixin, BaseEarthCard):
    name = "Nature's Fury"
    _mana_cost = 6
    spell = True
    
    def summon_actions(self, *args, **kwargs):
        damages = []
        for slot_id, slot in self.player.slots.items():
            if slot.card is not None:
                damages.append(slot.card.attack)
        damages = sorted(damages, reverse = True)
        total_damage = sum(damages[:2])
        yield SpecialAttack(doer = self, target = self.player.opponent, damage = total_damage, stage = "summon", *args, **kwargs)

class ForestSpider(BaseEarthCard):
    name = "Forest Spider"
    _mana_cost = 0
    _attack = 2
    _life = 11

class GiantSpider(BaseEarthCard):
    name = "Giant Spider"
    _mana_cost = 7
    _attack = 4
    _life = 24

    def summon_actions(self, *args, **kwargs):
        neighbours = self.slot.get_neighbours()
        for neighbour in neighbours:
            if neighbour.card is None:
                AddCard(doer = self, target = self.slot.player,slot_id = neighbour.slot_id, card_name = "Forest Spider", stage = "summon")

class Troll(BaseEarthCard):
    name = "Troll"
    _mana_cost = 8
    _attack = 6
    _life =26

    def start_of_owner_turn_actions(self, *args, **kwargs):
        yield Heal(doer = self, target = self, health = 4, *args, **kwargs)

class StoneRain(SpellMixin, BaseEarthCard):
    name = "Stone Rain"
    _mana_cost = 9
    spell = True

    def summon_actions(self, *args, **kwargs):
        player = self.player
        opponent = player.opponent
        for slot_id, slot in player.slots.items():
            if slot.card is not None:
                yield SpecialAttack(doer = self, target = slot.card, damage = 25, stage = "summon", *args, **kwargs)
        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                yield SpecialAttack(doer = self, target = slot.card, damage = 25, stage = "summon", *args, **kwargs)

class EarthElemental(BaseEarthCard):
    name = "Earth Elemental"
    _mana_cost = 10
    _life = 50

    @managed_by_buff
    @property
    def attack(self):
        return self.slot.player.get_mana(self.type)
    
    def summon_actions(self, *args, **kwargs):
      
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

class MasterHealer(BaseEarthCard):
    name = "Master Healer"
    _mana_cost = 11
    _attack = 3
    _life = 34

    def start_of_owner_turn_actions(self, *args, **kwargs):
        yield Heal(doer = self, target = self.slot.player, health = 3, stage = "start of owner turn", *args, **kwargs)
        for slot_id, slot in self.slot.player.slots.items:
            if slot.card is not None:
                yield Heal(doer = self, target = slot.card, health = 3, stage = "start of owner turn", *args, **kwargs)

class Hydra(BaseEarthCard):
    name = "Hydra"
    _mana_cost = 12 
    _attack = 3
    _life = 40

    def start_of_owner_turn_actions(self, *args, **kwargs):
        yield Heal(doer = self, target = self, health = 4, stage = "start of owner turn", *args, **kwargs)

    def turn_actions(self, *args, **kwargs):
        yield BasicAttack(doer = self, target = self.slot.player.opponent, damage = self.attack, stage = "turn", *args, **kwargs)
        for slot_id, slot in self.slot.player.opponent.slots.items():
            if slot.card is not None:
                yield BasicAttack(doer = self, target = slot.card, damage = self.attack, stage = "turn", *args, **kwargs)
