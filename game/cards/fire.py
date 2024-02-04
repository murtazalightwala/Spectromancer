from game.cards import BaseCard, SpellMixin
from game.actions import *
from game.buff import BaseBuff, managed_by_buff
from game.slot import Slot

class BaseFireCard(BaseCard):
    type = "fire"

class GoblinBerserker(BaseFireCard):
    name = "Goblin Berserker"
    _mana_cost = 1
    _attack = 4
    _life = 16

    def start_of_owner_turn_actions(self, *args, **kwargs):
        for neighbour in self.slot.get_neighbours():
            card = neighbour.card
            if card is not None:
                yield SpecialAttack(damage = 2, doer = self, target = card, stage = "start_of_owner_turn", *args, **kwargs)

class WallOfFire(BaseFireCard):
    name = "Wall Of Fire"
    _mana_cost = 2
    _attack = 0
    _life = 5
    wall = True

    def summon_actions(self, *args, **kwargs):
        opponent = self.slot.player.opponent
        for slot_id, card in opponent.slots.values:
            yield SpecialAttack(damage = 5, doer = self, target = card, stage = "summon", *args, **kwargs)

class PriestOfFire(BaseFireCard):
    name = "Priest Of Fire"
    _mana_cost = 3
    _attack = 3
    _life = 13

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


class FireDrake(BaseFireCard):

    name = "Fire Drake"
    _mana_cost = 4
    _attack = 4
    _life = 18

    def summon_actions(self, *args, **kwargs):
        return super().turn_actions(*args, **kwargs)

class OrcChiefTain(BaseFireCard):

    name = "Orc Chieftain"
    _mana_cost = 5
    _attack = 3
    _life = 17
    buffs = []

    def summon_actions(self, *args, **kwargs):

        def f(attack):
            _output = attack + 2
            return _output        
        
        def buff_function(target):
            if isinstance(target, Slot):
                return
            elif target.wall:
                return
            BaseCard.attack.get_or_create_instance(target).apply_buff(f)
        
        def debuff_function(target):
            if isinstance(target, Slot):
                return
            elif target.wall:
                return
            BaseCard.attack.get_or_create_instance(target).remove_buff(f)
        
        neighbours = self.slot.get_neighbours()
        for neighbour in neighbours:
            buff = BaseBuff(self, neighbour, buff_function, debuff_function, *args, **kwargs)
            self.buffs.append(buff)
            yield ApplyBuff(buff = buff, doer = self, target = neighbour, stage = "summon", *args, **kwargs)

class FlameWave(SpellMixin, BaseFireCard):
    name = "Flame Wave"
    spell = True
    _mana_cost = 6

    def summon_actions(self, *args, **kwargs):
        opponent = self.player.opponent
        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                yield SpecialAttack(damage = 9, doer = self, stage = "summon", target = slot.card, *args, **kwargs)

class MinotaurCommander(BaseFireCard):
    name = "Minotaur Commander"
    _mana_cost = 7
    _attack = 6
    _life = 20

    def summon_actions(self, *args, **kwargs):
        
        def f(attack):
            return attack  + 2
        
        
        def buff_function(target):
            if isinstance(target, Slot):
                return
            elif target.wall:
                return
            BaseCard.attack.get_or_create_instance(target).apply_buff(f)
        
        def debuff_function(target):
            if isinstance(target, Slot):
                return
            elif target.wall:
                return
            BaseCard.attack.get_or_create_instance(target).remove_buff(f)
        
        
        owner = self.slot.player
        for slot_id, slot in owner.slots.items():
            buff = BaseBuff(self, slot, buff_function, debuff_function, *args, **kwargs)
            self.buffs.append(buff)
            yield ApplyBuff(buff = buff, doer = self, target = slot, stage = "summon", *args, **kwargs)

class Bargul(BaseFireCard):
    name = "Bargul"
    _mana_cost = 8
    _attack = 8
    _life = 26

    def summon_actions(self, *args, **kwargs):
        owner = self.slot.player
        opponent = owner.opponent

        for slot_id, slot in owner.slots.items():
            if slot.card is not None:
                yield SpecialAttack(doer = self, target = slot.card, damage = 4, stage = "summon", *args, **kwargs)
        
        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                yield SpecialAttack(doer = self, target = slot.card, damage = 4, stage = "summon", *args, **kwargs)
        
class Inferno(SpellMixin, BaseFireCard):
    name = "Inferno"
    spell = True
    _mana_cost = 9

    def summon_actions(self, target = None, *args, **kwargs):
        if target is not None:
            yield SpecialAttack(damage = 18, doer = self, target = target, stage = "summon", *args, **kwargs)
        opponent = self.slot.player.opponent
        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                yield SpecialAttack(damage = 10, doer = self, target = target, stage = "summon", *args, **kwargs)

class FireElemental(BaseFireCard):
    name = "Fire Elemental"
    _mana_cost = 10
    _life = 37

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
    
class Armageddon(SpellMixin, BaseFireCard):
    name = "Armageddon"
    _mana_cost = 11 
    spell = True

    def summon_actions(self, *args, **kwargs):
        opponent = self.player.opponent
        damage = 8 + self.player.get_mana(self.type)
        yield SpecialAttack(damage = damage, doer = self, target = opponent, stage = "summon", *args, **kwargs)
        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                yield SpecialAttack(damage = damage, doer = self, target = slot.card, stage = "summon", *args, **kwargs)
        for slot_id, slot in self.player.slots.items():
            if slot.card is not None:
                yield SpecialAttack(damage = damage, doer = self, target = slot.card, stage = "summon", *args, **kwargs)

class Dragon(BaseFireCard):
    name = "Dragon"
    _mana_cost = 12
    _attack = 9
    __life = 40

    def summon_actions(self, *args, **kwargs):

        def f(func):
                def _func(_obj, card_name, slot_id, *args, **kwargs):
                    _output = func(_obj, card_name, slot_id, *args, **kwargs)
                    for summon_action  in _output:
                        if summon_action.doer.spell:
                            summon_action.damage += summon_action//2
                    return _output
                return _func
       
        def buff_function(target):
            target.play_card.apply_buff(f)
        
        def debuff_function(target):
            target.play_card.remove_buff(f)
        
        buff = BaseBuff(self, self.slot.player, buff_function, debuff_function, *args, **kwargs)
        self.buffs = [buff]
        
        yield ApplyBuff(buff = buff, doer = self, target = self.slot.player, stage = "summon", *args, **kwargs)

