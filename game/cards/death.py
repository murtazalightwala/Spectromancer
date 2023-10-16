from game.cards import BaseCard, SpellMixin, CardMap
from game.actions import *
from game.buff import BaseBuff, managed_by_buff
from game.slot import Slot

class BaseDeathCard(BaseCard):
    type = "death"


class DarkRitual(SpellMixin, BaseDeathCard):
    name = "Dark Ritual"
    _mana_cost = 1
    spell = True

    def summon_actions(self, *args, **kwargs):
        player = self.player
        opponent = player.opponent

        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                    yield SpecialAttack(doer = self, target = slot.card, damage = 3, stage = "summon", *args, **kwargs)

        for slot_id, slot in player.slots.items():
            if slot.card is not None:
                    yield Heal(doer = self, target = slot.card, health = 3, stage = "summon", *args, **kwargs)

class CursedFog(SpellMixin, BaseDeathCard):
    name = "Cursed Fog"
    _mana_cost = 2
    spell = True

    def summon_actions(self, *args, **kwargs):
        player = self.player
        opponent = player.opponent
        yield SpecialAttack(doer = self, target = opponent, damage = 3, stage = "summon", *args, **kwargs)
        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                    yield SpecialAttack(doer = self, target = slot.card, damage = 12, stage = "summon", *args, **kwargs)

class Banshee(BaseDeathCard):
     name = "Banshee"
     _mana_cost = 3
     _attack = 4
     _life = 21

     def summon_actions(self, *args, **kwargs):
        opponent = self.slot.player.opponent
        opposing_creature = opponent.slots[self.slot.slot_id].card
        if opposing_creature is None:
             return []
        damage = opposing_creature.life//2
        yield SpecialAttack(doer = self, target = opposing_creature, damage = damage, stage = "summon", *args, **kwargs)

class EmissaryOfDorlak(BaseDeathCard):
    name = "Emissary of Dorlak"
    _mana_cost = 4
    _attack = 7
    _life = 48

    def __init__(self, slot, *args, **kwargs):
         if slot.card is None:
              raise Exception("Emissary of Dorlak can only be summoned on onwer's existing creatures")
         slot.remove_card()
         super().__init__(slot, *args, **kwargs)

class BloodRitual(SpellMixin, BaseDeathCard):
    name = "Blood Ritual"
    _mana_cost = 5
    
    def summon_actions(self, target, *args, **kwargs):
        damage = min(32, target.life)
        target.slot.remove_card()
        for slot_id, slot in self.player.opponent.slots.items():
             if slot.card is not None:
                yield SpecialAttack(doer = self, target = slot.card, damage = damage, stage = "summon", *args, **kwargs)

class KeeperOfDeath(BaseDeathCard):
    name = "Keeper of Death" 
    _mana_cost = 6
    _attack = 7
    _life = 35
    buffs = list()

    def summon_actions(self, *args, **kwargs):
        
        def f(func):
            def _func(_obj, *args, **kwargs):
                _output = func(_obj, *args, **kwargs)
                _obj.slot.player.opponent.increase_mana(self.type, 1)
                return _output
            return _func
        
        def buff_function(target):
            if isinstance(target, BaseCard):
                target.death_actions.add_buff(f)
        
        def debuff_function(target):
            if isinstance(target, BaseCard):
                target.death_actions.remove_buff(f)

        for slot_id, slot in self.slot.player.slots.items():
            buff = BaseBuff(doer = self, target = slot, buff_function = buff_function, debuff_function = debuff_function, *args, **kwargs)
            self.buffs.append(buff)
            yield ApplyBuff(doer = self, target = slot, buff = buff, stage = "summon", *args, **kwargs)
        
class DrainSouls(SpellMixin, BaseDeathCard):
    name = "Drain Souls"
    spell = True
    _mana_cost = 7

# Kill all creatures. Drain Souls heals
# an amount of life to its caster equal to
# twice the number of creatures killed by
# this spell. When Drain Souls is cast it is
# replaced by the Rage of Souls spell card.

    def summon_actions(self, *args, **kwargs):
        player = self.player
        opponent = player.opponent
        creature_count = 0
        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                yield KillCard(doer = self, target = slot.card, slot = slot, stage = "summon", *args, **kwargs)
                creature_count += 1
        yield Heal(doer = self, target = player, health = creature_count * 2, stage = "summon", *args, **kwargs)

class MasterLich(BaseDeathCard): 
    name = "Master Lich"
    _mana_cost = 8
    _attack = 8
    _life = 46

# When Master Lich is summoned it deals 8
# damage to each of the opponent's creatures.
# Each time Master Lich deals damage
# to the opponent, it increases
# its owner's Death power by 2. 

    def summon_actions(self, *args, **kwargs):

        player = self.slot.player
        opponent = player.opponent

        for slot_id, slot in opponent.slots.items():
            if slot.card is not None:
                yield SpecialAttack(doer = self, target = slot, damage = 8, stage = "summon", *args, **kwargs)

    def turn_actions(self, *args, **kwargs):
        opponent = self.slot.player.opponent
        hitting_opponent = False
        if opponent.slots[self.slot.slot_id].card is None:
            hitting_opponent = True
        _output = [x for x in super().turn_actions(*args, **kwargs)]
        if hitting_opponent:
            _output.append(ManaIncrease(doer = self, target = self.slot.player, element = self.type, stage = "turn", *args, **kwargs))
        return _output
        