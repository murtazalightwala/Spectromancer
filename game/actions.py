from abc import abstractmethod

class BaseAction:
    """
    This class represents implementation of base action class. Each action will have a doer and a target.
    Doers and targets can be player, slot or card. 
    """

    type:str

    def __init__(self, doer, target, stage, *args, **kwargs):
        self.doer = doer
        self.target = target
        self.stage = stage

    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

class BasicAttack(BaseAction):

    type = "BasicAttack"

    def __init__(self, damage, *args, **kwargs):
        super().__init__(**kwargs)
        self.damage = damage

    def __call__(self, *args, **kwargs):
        self.target.take_damage(self.damage, type = "BasicAttack", stage = self.stage)

class SpecialAttack(BaseAction):

    type = "SpecialAttack"

    def __init__(self, damage, *args, **kwargs):
        super().__init__(**kwargs)
        self.damage = damage

    def __call__(self, *args, **kwargs):
        self.target.take_damage(self.damage, type = "SpecialAttack", stage = self.stage)

class ApplyBuff(BaseAction):

    type = "ApplyBuff"

    def __init__(self, buff, *args, **kwargs):
        super().__init__(**kwargs)
        self.buff = buff
        
    def __call__(self, *args, **kwargs):
        self.buff.apply_buff(self.buff.target, *args, **kwargs)

class ApplyDebuff(BaseAction):

    type = "ApplyDebuff"

    def __init__(self, buff, *args, **kwargs):
        super().__init__(**kwargs)
        self.buff = buff
    
    def __call__(self, *args, **kwargs):
        self.buff.apply_debuff(self.buff.target, *args, **kwargs)

class Heal(BaseAction):
    
    type = "Heal"

    def __init__(self, health, *args, **kwargs):
        super().__init__(**kwargs)
        self.health = health

    def __call__(self, *args, **kwargs):
        self.target.get_healed(self.health, stage = self.stage)

    
class ManaDrain(BaseAction):

    type = "ManaDrain"

    def __init__(self, element, decrease, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element = element
        self.decrease = decrease

    def __call__(self, *args, **kwargs):
        self.target.mana_drain(self.element, self.decrease, stage = self.stage, type = self.type)

class ManaIncrease(BaseAction):

    type = "ManaIncrease"

    def __init__(self, element, increase, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element = element
        self.increase = increase

    def __call__(self, *args, **kwargs):
        self.target.mana_increase(self.element, self.increase, stage = self.stage, type = self.type)
    
class DeckShuffle(BaseAction):

    type = "DeckShuffle"

    def __init__(self, element = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if element is not None:
            self.element = element
        else:
            self.element = "All"
                
    @staticmethod
    def shuffle_element(player, element, *args, **kwargs):
        player.shuffle_deck(element)

    def __call__(self, *args, **kwargs):
        if self.element == "All":
            for element in self.target.mana:
                self.shuffle_element(self.target, element)
        else:
            self.shuffle_element(self.target, self.element)
    
class AddCard(BaseAction):

    type = "AddCard"

    def __init__(self, slot_id, card_name, replace = False, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.slot_id = slot_id
        self.card_name = card_name
        self.replace = replace

    def __call__(self, *args, **kwargs):
        from game.cards import CardMap

        if self.target.slots[self.slot_id].is_empty:
            self.target.slots[self.slot_id].set_card(CardMap.get_card_by_name(self.card_name, player = self.target, slot = self.target.slots[self.slot_id], slot_id = self.slot_id))
        elif self.replace:
            self.target.slots[self.slot_id].set_card(CardMap.get_card_by_name(self.card_name, player = self.target, slot = self.target.slots[self.slot_id], slot_id = self.slot_id))
    
class RemoveCard(BaseAction):

    type = "RemoveCard"

    def __init__(self, slot_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slot_id = slot_id

    def __call__(self, *args, **kwargs):
        self.target.slot[self.slot_id].remove_card()

class MoveCard(BaseAction):

    type = "MoveCard"

    def __init__(self, _from, _to, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._from = _from
        self._to = _to

    def __call__(self, *args, **kwargs):
        if not self.target.slots[self._from].is_empty:
            if self.target.slots[self._to].is_empty:
                card = self.target.slots[self._from].remove_card()
                card.slot_id = self._to
                card.slot = self.target.slots[self._to]
                self.target.slots[self._to].set_card(card)

class KillCard(BaseAction):

    type = "KillCard"

    def __init__(self, slot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slot = slot
    
    def __call__(self, *args, **kwargs):
        killed_card = self.slot.remove_card()
        death_actions = [x for x in killed_card.death_actions()]
        for action in death_actions:
            action()

