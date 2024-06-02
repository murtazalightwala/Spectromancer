from game.game import BaseGame
from game.player import BasePlayer
import sys


module = sys.modules[__name__]

def setup_module():
    module.player_1 = BasePlayer("Test Player 1", "death")
    module.player_2 = BasePlayer("Test Player 2", "chaos")
    module.game = BaseGame(module.player_1, module.player_2) 



# os.path.append()

class TestGame:
    def test_game_created(cls):
        assert module.game is not None, "Game not created!!!"
    
    def test_game_objects_player_1_correctly_initialized(cls):
        assert module.game.player_1 == module.player_1, "Player 1 is set up wrong!!!"
        
    def test_game_objects_player_2_correctly_initialized(cls):
        assert module.game.player_2 == module.player_2, "Player 2 is set up wrong!!!"
        
    def test_game_objects_is_ended_correctly_initialized(cls):
        assert module.game.is_ended == False, "'is_ended' is set up wrong!!!"

    def test_player_1_name_correctly_initialized(cls):
        assert module.player_1.name == "Test Player 1", "Player 1 name is set up wrong!!!"
        
    def test_player_2_name_correctly_initialized(cls):
        assert module.player_2.name == "Test Player 2", "Player 2 name is set up wrong!!!"

    def test_player_1_special_correctly_initialized(cls):
        assert module.player_1.special == "death", "Player 1 special set up wrong!!!"

    def test_player_2_name_correctly_initialized(cls):
        assert module.player_2.special == "chaos", "Player 2 special set up wrong!!!"

        