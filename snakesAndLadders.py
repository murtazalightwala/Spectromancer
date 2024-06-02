import random

class Board:
    snakes = [
    (22, 4),
    (32, 13),
    (45, 14),
    (64, 39),
    (68, 47), 
    (94, 3),
    (99, 64)
]

    ladders = [
    (5, 27),
    (12, 33),
    (25, 43),
    (30, 49),
    (42, 81),
    (46, 67),
    (70, 92),
    (74, 95),
    (76, 97)
]

    @staticmethod
    def get_cell_top_left(cell):
        if ((cell - 1) // 10) %  2 == 0:
            x = 9 - ((cell -1) % 10)
        else:
            x = (cell - 1) % 10 
        y = (cell - 1) // 10
        return (x, y)
             
    def check_for_snake_or_ladder(self, player):
        self.check_for_snake(player)
        self.check_for_ladder(player)

    def check_for_snake(self, player):
        for snake in self.snakes:
            if player.position == snake[0]:
                print("bit by snake, moving from {} to {}".format(snake[0], snake[1]))
                player.position = snake[1]
        

    def check_for_ladder(self, player):
        for ladder in self.ladders:
            if player.position == ladder[0]:
                print("climbed a ladder, moving from {} to {}".format(ladder[0], ladder[1]))
                player.position = ladder[1]

    def draw_board(self, size = 500):

        padding = 10
        height = size
        width = size
        c = int(size/10)
        filename = "test.svg"
        
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                  .format(width + 2 * padding, height + 2 * padding,
                          -padding, -padding, width + 2 * padding, height + 2 * padding),
                  file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print('#snake {', file=f)
            print('    stroke: #555D50;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 15;\n}', file=f)
            print('#ladder {', file=f)
            print('    stroke: #F0E68C;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 15;\n}', file=f)
            print(']]></style>', file=f)
            print('</defs>', file=f)
            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(0, 10*c, 10*c, 10*c) , file = f)
            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(10*c, 0, 10*c, 10*c) , file = f)
            for i in range(10):
                print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(0, i*c, 10*c, i*c) , file = f)
                print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(i*c, 0,i*c, 10*c) , file = f)
            for i in range(1, 101):
                x, y = self.get_cell_top_left(i)
                print('<text x="{}" y="{}">{}</text>'.format(x*c + c/2,y*c + c/2 , i) , file = f)
            for snake in self.snakes:
                x1, y1 = self.get_cell_top_left(snake[0])
                x2, y2 = self.get_cell_top_left(snake[1])
                print('<line id="snake" x1="{}" y1="{}" x2="{}" y2="{}" opacity="0.25"/>'.format(x1*c + c/2, y1*c + c/2, x2*c + c/2, y2*c + c/2), file = f)    
            
            for ladder in self.ladders:
                x1, y1 = self.get_cell_top_left(ladder[0])
                x2, y2 = self.get_cell_top_left(ladder[1])
                print('<line id="ladder" x1="{}" y1="{}" x2="{}" y2="{}" opacity="0.5"/>'.format(x1*c + c/2, y1*c + c/2, x2*c + c/2, y2*c + c/2), file = f)    
            

            print('</svg>', file=f)
            

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 0

    def move(self, die_roll):
        self.position += die_roll

class Game:
    @staticmethod
    def roll_dice():
        return  random.randint(1, 6)

    
    def __init__(self, player_1, player_2, board):
        self.player_1 = player_1
        self.player_2 = player_2
        self.turn = player_1
        self.board = board

    def switch_turn(self):
        if self.turn == self.player_1:
            self.turn = self.player_2
        else:
            self.turn = self.player_1

    def check_if_ended(self):
        if self.player_1.position == 100 or self.player_2.position == 100:
            return True
        return False
        
    def play_round(self):
        self.play_turn()
        if self.check_if_ended():
            return {"winner": self.turn.name}
        self.switch_turn()
        self.play_turn()
        if self.check_if_ended():
            return {"winner": self.turn.name}
        self.switch_turn()
        print("{}'s position: {}".format(self.player_1.name, self.player_1.position))
        print("{}'s position: {}".format(self.player_2.name, self.player_2.position))
            

    def play_turn(self):
        input("{}'s turn".format(self.turn.name))
        die_roll = self.roll_dice()
        self.turn.move(die_roll)
        self.board.check_for_snake_or_ladder(self.turn)

    def play_game(self):
        self.player_1.position = 0
        self.player_2.position = 0
        while not self.check_if_ended():
            self.play_round()