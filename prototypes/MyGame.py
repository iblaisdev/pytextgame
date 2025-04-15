import random
import time
import sys
import os

##########################################################################
# TODO: break to different files
##########################################################################

##########################################################################
class Util:
    @staticmethod
    def rand(low: int, high: int): #inclusive
        return random.randint(low, high)

    @staticmethod
    def __init__():
        pass

    @staticmethod
    def print_slow(s: str):
        for letter in s:
            print(letter, end='')
            sys.stdout.flush()
            #time.sleep(.05)
    @staticmethod
    def clear_console():
        if (os.name == 'posix'):
            os.system('clear')
        else:
            os.system('cls')

    def __init__(self):
        pass


##########################################################################
class Player:
    def __init__(self):
        self.health = 100
        self.name = 'Anonymous Mouse'

##########################################################################
class PlayerClass:
    def __init__(self):
        self.type = ['Knight', 'Wizard', 'Rogue']

##########################################################################
class GameItems:
    def __init__(self):
        self.phy_offense = {'sword':    [1, 15],
                            'staff':    [1, 15]}
        self.int_offense = {'wand':     [1, 10],
                            'scroll':  [-3, 15]}
        self.dex_offense = {'dagger':   [1, 8],
                            'bow':      [1, 15]}
        self.defense =     {'shield':   [3, 3],
                            'helmet':   [3, 3]}

##########################################################################
class Inventory:
    def __init__(self):
        self.offense = {'dagger':   [1, 10]}
        self.defense = {}

##########################################################################
class State:
    def __init__(self):
        self.state = 'noncombat' #combat
        self.combat_options = ['item', 'run']
        self.noncombat_options = ['continue', 'search', 'hide', 'attack']

    def process(self, select: str):
        if (select == "fail"):
            pass
        elif (select == "continue"):
            pass
        elif (select == "search"):
            pass
        elif (select == "hide"):
            pass
        elif (select == "attack"):
            pass
        elif (select == "item"):
            pass
        elif (select == "run"):
            pass
        else:
            print ("\n\tDEBUG: user selected", select) # delete this later
        
    # from any user string return: attack, run, item, fail, continue (or QUIT)
    # combat: attack, run, hide, item
    #noncombat: search, continue, item
    def parse_input(self, user_input: str):
        match user_input.lower().split():
            case [*_, "hint"]:
                if (self.state == 'combat'):
                    print ("Perhaps you can attack, run, hide, or use an item?")
                else:
                    print ("Perhaps you can continue moving ahead, search the area, or use an item?")
            case [*_, "attack"] | [*_, "fight"]:
                return "attack"
            case [*_, "hide"] | [*_, "sneak"]:
                return "hide"
            case [*_, "run"] | [*_, "escape"] | [*_, "bail"]:
                if (self.state == 'combat'):
                    return "run"
                else: return "fail"
            case [*_, "use"] | [*_, "item"]:
                return "item"
            case [*_, "continue"] | [*_, "going"] | [*_, "ahead"]:
                if (self.state == 'noncombat'):
                    return "continue"
                else: return "fail"
            case [*_, "search"] | [*_, "look"] | [*_, "find"]:
                return "search"
            case [*_, "restart"]:
                print("restart NOT DONE YET") #TODO
            case [*_, "quit"] | [*_, "exit"]:
                quit()
            case _:
                return "fail"

##########################################################################
class Area:
    def __init__(self):
        self.game_intro = "\nWelcome to the wonderful world of [game-name-here]"
        self.background = "\n\n   You awake in a ...\n"
        self.area_intros = ["\nYou have entered Area X",
                            "\nYou have entered Area Y",
                            "\nYou have entered Area Z"]
        self.area_mobs = ["",
                          "Kobold",
                          "Dragon"]
    def get_area(self):
        return self.area_intros[Util.rand(0, len(self.area_intros) - 1)]

    def get_specific_area(self, index: int):
        return self.area_intros[index]

##########################################################################

a = Area()
p = Player()
i = Inventory()
s = State()

# show intro messages
Util.clear_console()
#Util.print.slow('What is your name')
Util.print_slow(a.game_intro)
Util.print_slow(a.background)

print(a.get_specific_area(0))

# start game loop
while True:
    str = "\nWhat would you like to do?\n\n"
    user_input = input(str)
    select = s.parse_input(user_input) # 'continue', 'search', 'hide', 'attack', 'item', 'run'
    s.process(select)
   