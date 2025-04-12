import random
import json
import time
import sys
import os

##########################################################################
class Util:

    print_speed_default = .05
    print_speed = .05

    @staticmethod
    def __init__():
        pass

    @staticmethod
    def print_slow(s: str, addquotes: bool):
        if addquotes == True:
            print("\"", end='')
        for letter in s:
            print(letter, end='')
            sys.stdout.flush()
            if Util.print_speed > 0.0:
                time.sleep(Util.print_speed)
        if addquotes == True:
            print("\"")

    @staticmethod
    def clear_console():
        if (os.name == 'posix'):
            os.system('clear')
        else:
            os.system('cls')

    def __init__(self):
        pass

##########################################################################
class State:
    def __init__(self):
        self.stateid = 'id-game-start'
        self.gamedata = {}
        self.debug_objects = False
        self.debug_time = False

    def set_debug_objects(self, state: bool):
        print(f"\nDebug mode setting: {state}\n")
        self.debug_objects = state

    def set_debug_time(self, state: bool):
        print(f"\nDebug time setting: {state}\n")
        self.debug_time = state
        if state == True:
            Util.print_speed = 0.0
        else:
            Util.print_speed = Util.print_speed_default

    def load_game_data(self):
        self.gamedata = {} # {"id-game-start" : {"prompt_text": "(Run or pass)","parse_input": ["run", "pass"], "run" : "id-forest-start", "pass" : "id-forest-blah"}}
        with open('game.json') as json_file:
            self.gamedata = json.load(json_file)
        with open('forest.json') as json_file:
            self.gamedata.update(json.load(json_file))
        if self.debug_objects == True:
            print(self.gamedata) #dump full game dictionary

    def roll_dice(self, roll_data_list):
        minval = roll_data_list[0] # e.g., 1
        maxval = roll_data_list[1] # e.g., 20
        chkval = roll_data_list[2] # e.g., 13
        result = random.randint(minval, maxval)
        if result > chkval:
            Util.print_slow(f"\nYou rolled a {result}, which succeeds.\n\n", False)
            return 'roll_success'
        else:
            Util.print_slow(f"\nYou rolled a {result}, which fails.\n\n", False)
            return 'roll_failure'

    def process_input(self, prompt_text: str, allowed_actions):
        allowed_actions.append('restart')
        while True:
            user_entered_txt = input("\n" + prompt_text + "\n\n>>> ")
            clean_input = self.__sanitize_input(user_entered_txt)
            if self.debug_objects == True:
                print(f"user_entered_txt: {user_entered_txt}\nclean_input: {clean_input}")
            for action in allowed_actions:
                if action == clean_input:
                    return action # e.g., 'run'
            print('Not an answer bub')

    # parse user input to allowed values
    def __sanitize_input(self, user_input: str):
        words = user_input.lower().split()
        if self.debug_objects == True:
            print(f"split: {words}")
        result = "fail"
        for word in words:
            match word:
                case "talk":
                    return "talk"
                case "fight":
                    return "fight"
                case "run":
                    return "run"
                case "ambush":
                    return "ambush"
                case "yes":
                    return "yes"
                case "no":
                    return "no"
                case "pass":
                    return "pass"
                case "hide":
                    return "hide"
                case "restart":
                    return "restart"
                case "debugobj":
                    self.set_debug_objects(True)
                    return "fail"
                case "debugtime":
                    self.set_debug_time(True)
                    return "fail"
                case "ndebug":
                    self.set_debug_objects(False)
                    self.set_debug_time(False)
                    return "fail"
                case _:
                    return "fail"

##########################################################################
##########################################################################
##########################################################################

# create state
state = State()

# set debug options if needed
if len(sys.argv) > 1:
    print (sys.argv[1])
    if sys.argv[1] == "debugobj":
        state.set_debug_objects(True)
    elif sys.argv[1] == "debugtime":
        state.set_debug_time(True)
    if len(sys.argv) > 2:
        if sys.argv[2] == "debugobj":
            state.set_debug_objects(True)
        elif sys.argv[2] == "debugtime":
            state.set_debug_time(True)

# load game data dictionaries
state.load_game_data()

# clear console
if state.debug_objects != True:
    Util.clear_console()

# start game loop
while True:

    # get current game state - node is a sub-dictionary
    node = state.gamedata.get(state.stateid, None)

    if (node == None):
        # make sure we have that state map entry!
        print(f"\n\t *** Critical error: '{state.stateid}' not found in gamedata map ***\n")
        time.sleep(10)
        quit()

    else: # process the game node

        if state.debug_objects == True:
            print()
            print('*' * 120)
            print(f"CURRENT_NODE: {node}")
            print('*' * 120)
            print()

        # print intro text for this event
        val = node.get('intro_text', None) # val is either None, or a list of strings
        if val != None:
            for entry in val:
                Util.print_slow(entry, True)

        # see if this is a goto node
        val = node.get('goto_node', None) # val is either None, string name for next state
        if val != None:
            if val == 'id-game-quit':
                quit()
            elif val == 'id-game-goto-restart':
                Util.clear_console()
            state.stateid = val

        # see if there is a prompt text and parse_input entry
        prompt_text = node.get('prompt_text', None)
        parse_input = node.get('parse_input') # list of action strings

        if parse_input != None:

            # get user input choice, make sure it's a alloed key for this node
            action_key = state.process_input(prompt_text, parse_input) # e.g. 'run'

            # assign new state id base on that node key, but allow 'restart' always
            if action_key == 'restart':
                state.stateid = 'id-game-restart'
            else:
                state.stateid = node[action_key]

            print() #newline

        elif prompt_text != None:

            input("\n" + prompt_text + "\n\n>>> ")


        # see if we need to roll any dice
        roll_data_list = node.get('roll_dice', None) # e.g., [1, 20, 10]
        if roll_data_list != None:
            roll_result = state.roll_dice(roll_data_list) # e.g., roll_success

            # assign new state id base on that roll result
            state.stateid = node[roll_result]

        if state.debug_objects == True:
            print(f"\n  |Newly assigned node: {state.stateid}|\n")

##########################################################################
##########################################################################
##########################################################################
