from game.cards import BaseCard
from typing import Any

class BaseBuff:
    def __init__(self, doer, target, buff_function, debuff_function, *args, **kwargs):
        self.doer = doer
        self.target = target
        self.buff_function = buff_function
        self.debuff_function = debuff_function

    def apply_buff(self, target = None):
        if target is None:
            target = self.target
        self.buff_function(target)
        self.doer.buffs_doer.add(self)
        target.buffs_target.add(self)

    def apply_debuff(self, target = None):
        if target is None:
            target = self.target
        self.debuff_function(target)
        self.doer.buffs_doer.remove(self)
        target.buffs_target.remove(self)
    
