from game.cards import BaseCard, SpellMixin, CardMap
from game.actions import *
from game.buff import BaseBuff, managed_by_buff
from game.slot import Slot
import random

class BaseChaosCard(BaseCard):
    type = "chaos"

class InsanianPeacekeeper(BaseChaosCard):
    name = "Insanian Peacekeeper"
    _mana_cost = 1
    _attack = 4
    _life = 11

    """
At the beginning of its owner's turn,
Insanian Peacekeeper heals 1-6 life
to its owner.
"""

    def start_of_owner_turn_actions(self, *args, **kwargs):
       yield Heal(doer = self, target = self.slot.player, health = random.randint(1, 6)) 


class InsanianBerserker(BaseChaosCard):
    name = "Insanian Berserker"
    _mana_cost = 2
    _attack = 4
    _life = 14

    """
At the beginning of its owner's turn,
Insanian Berseker deals 1-6 damage
to the opponent.
"""

    def start_of_owner_turn_actions(self, *args, **kwargs):
        yield SpecialAttack(damage = random.randint(1, 6), doer = self, target = self.slot.player.opponent, stage = "start_of_owner_turn")


class DoomBolt(SpellMixin, BaseChaosCard):
    name = "Doom Bolt"
    spell = True
    _mana_cost = 3

    """
Doom Bolt deals 25 damage to
a random opponent's creature.  
    """
    def summon_actions(self, *args, **kwargs):
        opponent_cards = [slot.card for slot in self.slot.player.opponent.slots if slot.card is not None]
        yield SpecialAttack(damage = 25, doer = self, target = random.choice(opponent_cards), stage = "summon", *args, **kwargs)

class ChaoticWave(SpellMixin, BaseChaosCard):
    name = "Chaotic Wave"
    spell = True
    _mana_cost = 4

"""
Chaotic Wave deals 2-12 damage to each
of the opponent's creatures, then heals
2-12 life to each of its caster's creatures.
"""
    def summon_actions(self, *args, **kwargs):
        opponent_slots = [slot.card for slot in self.slot.player.opponent.slots if slot.card is not None]
        for slot in opponent_slots:
            yield SpecialAttack(damage = random.randint(2, 12), doer = self, target = slot, stage = "summon")
        for slot in self.slot.player.slots:
            if slot.card is not None:
                yield Heal(doer = self, target = slot, health = random.randint(2, 12))


class InsanianShaman(BaseChaosCard):
    name = "InsanianShaman"
    _mana_cost = 5
    _attack = 3
    _life = 25

"""
At the beginning of its owner's turn,
Insanian Shaman decreases a random
opponent's power by 2.
    """

    def start_of_owner_turn_actions(self, *args, **kwargs):
        yield ManaDrain(random.choice(self.slot.player.opponent.element_list), 2, stage = "start_of_owner_turn", *args, **kwargs)

class InsanianLord(BaseChaosCard):
    name = "Insanian Lord"
    _mana_cost = 6 
    _attack = 6
    _life = 28

    """
    At the beginning of its owner's turn,
Insanian Lord increases a random
owner's power by 2.
    """

    def start_of_owner_turn_actions(self, *args, **kwargs):
        yield ManaIncrease(random.choice(self.slot.player.element_list), 2, stage = "start_of_owner_turn", *args, **kwargs)

class InsanianCatapult(BaseChaosCard):
    name = "Insanian Catapult"
    _mana_cost = 7
    _attack = 6
    _life = 38

    def start_of_owner_turn_actions(self, *args, **kwargs):
        opponent_slots = [slot.card for slot in self.slot.player.opponent.slots if slot.card is not None]
        yield SpecialAttack(damage = 10, doer = self, target = random.choice(opponent_slots), stage = "start_of_owner_turn")


class InsanianSoldier(BaseChaosCard):
    name = "Insanian Soldier"
    _mana_cost = 0
    _attack = 4
    _life = 15


class InsanianKing(BaseChaosCard):
    name = "Insanian King"
    _mana_cost = 8
    _attack = 6
    _life = 46


"""
At the end of its owner's turn,
Insanian King puts a 4/15 Soldier
into a random empty slot.
"""

    def end_of_owner_turn_actions(self, *args, **kwars):
        pass
