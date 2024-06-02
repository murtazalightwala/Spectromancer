from .basecard import *
from .air import *
from .death import *
from .earth import *
from .fire import *
from .water import *



class CardMap:
    card_map = {}

    @classmethod
    def get_card_by_name(cls, card_name, *args, **kwargs):
        return cls.card_map.get(card_name, BaseCard)(*args, **kwargs)
    
    @classmethod
    def get_card_info(cls, card_name, *args, **kwargs):
        card = cls.get_card_by_name(card_name)
        mana_cost = card.mana_cost
        life = card.life
        attack = card.attack
        _type = card.type
        return {"attack":attack, "life":life, "mana_cost": mana_cost, "type": _type}
    