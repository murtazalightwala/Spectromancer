
special_mapping = {
    "Death": "death",
    "Chaos": "chaos"
}

class BasePlayer:
    element_list = ["fire", "water", "air", "earth"]

    def __init__(self, name, special) -> None:
        self.name = name
        self.special = special
        self.element_list.append(special_mapping.get(special))
        self.mana = {}
        self.mana_inc = {}

    def build_by_config(self, game_config):
        game_config.configure_player(self)

    def set_mana(self, element, value = None):
        if value == None:
            value = self.mana.get(element, 0) + self.mana_inc.get(element, 0)
        self.mana[element] = value

    def set_mana_inc(self, element, value = 1):
        self.mana_inc[element] = value

