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
        return super().start_of_owner_turn_actions(*args, **kwargs)