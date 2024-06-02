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
    

class BuffManager:

    def __init__(self, function, instance = None, *args, **kwargs):
        self.function = function
        if instance is not None:
            self.instance = instance
            self.buffs = list()
        else:
            self.instances = {}
        self.is_property = False
        if isinstance(self.function, property):
            self.is_property = True
        

    def get_or_create_instance(self, _obj, *args, **kwargs):
        if _obj not in self.instances:
            self.instances[_obj] = BuffManager(self.function, _obj)
        return self.instances[_obj]


    def __get__(self, instance, owner):
        if instance is None:
            return self
        print("Call hota bhai!!!")
        return self.get_or_create_instance(instance)
        

    def add_buff( self, buff, _obj = None, *args, **kwargs):
        if _obj == None:
            _obj = self
        _obj.buffs.append(buff)
        
    def remove_buff(self, buff, _obj = None, *args, **kwargs):
        if _obj == None:
            _obj = self
        _obj.buffs.remove(buff)

    def __call__(self, *args, **kwargs):
        
        f = self.function
        for item in self.buffs:
            f = item(f)
        return f(self.instance,*args, **kwargs)
        
def managed_by_buff(function, *args, **kwargs):
    if isinstance(function, property):
        print("property hai!!!!")
        buff_manager = PropertyBuffManager(function)
    else:
        buff_manager = BuffManager(function)
    return buff_manager

class PropertyBuffManager(BuffManager):
    def __get__(self, instance, owner):
        
        if instance is None:
            return self
        f = self.get_or_create_instance(instance).function.fget(instance)
        for item in self.get_or_create_instance(instance).buffs:
            f = item(f)
        return f
   