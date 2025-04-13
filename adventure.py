import random
import json
import time
import sys
import os

##########################################################################
class Util:

    print_speed_default = .04
    print_speed = .04

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
class Player:
    def __init__(self):
        self.archetypes = ['knight', 'wizard', 'rogue']
        self.archetype = None;

    def get_stat_roll_modifier(self, roll_stat_list):
        mod = 0
        for stat in roll_stat_list: #e.g. ["constitution","strength"]
            if stat == 'constitution' and self.archetype == 'knight':
                mod += 1
            if stat == 'strength' and self.archetype == 'knight':
                mod += 1
            if stat == 'intelligence' and self.archetype == 'wizard':
                mod += 1
            if stat == 'wisdom' and self.archetype == 'wizard':
                mod += 1
            if stat == 'dexterity' and self.archetype == 'rogue':
                mod += 1
            if stat == 'charisma' and self.archetype == 'rogue':
                mod += 1
        return mod

##########################################################################
class State:
    def __init__(self):
        self.stateid = 'id-game-start'
        self.gamedata = {}
        self.debug_objects = False
        self.debug_time = False
        self.player = Player()
        self.inventory = [] #['example-item']

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

    def get_item_roll_modifier(self, roll_item_list_pairs): # e.g., [["good-item", 2], ["bad-item", -4]]
        mod = 0
        for lst in roll_item_list_pairs:
            item = lst[0]
            val = lst[1]
            if item in self.inventory:
                mod += val
        return mod

    def roll_dice(self, roll_data_list, roll_stat_list, roll_item_list_pairs):

        minval = roll_data_list[0] # e.g., 1
        maxval = roll_data_list[1] # e.g., 20
        chkval = roll_data_list[2] # e.g., 13
        result = random.randint(minval, maxval)
        statmod = self.player.get_stat_roll_modifier(roll_stat_list)
        itemmod = self.get_item_roll_modifier(roll_item_list_pairs)
        result += statmod + itemmod
        sign = '+' if itemmod >= 0 else '-'
        itemmod = abs(itemmod)
        if result > chkval:
            if (not roll_item_list_pairs):
                Util.print_slow(f"\nYou rolled {result} (+{statmod} class), which succeeds.\n\n", False)
            else:
                Util.print_slow(f"\nYou rolled {result} (+{statmod} class, {sign}{itemmod} items), which succeeds.\n\n", False)
            return 'roll_success'
        else:
            if (not roll_item_list_pairs):
                Util.print_slow(f"\nYou rolled {result} (+{statmod},+{itemmod}), which fails.\n\n", False)
            else:
                Util.print_slow(f"\nYou rolled {result} (+{statmod} class, {sign}{itemmod} items), which fails.\n\n", False)
            return 'roll_failure'

    def process_input(self, prompt_text: str, allowed_actions):
        allowed_actions.extend(['restart', 'faster', 'slower', 'fastest'])
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
                case "faster":
                    return "faster"
                case "fastest":
                    return "fastest"
                case "slower":
                    return "slower"
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

    # ask user what class they want to play
    def prompt_for_archetype(self):
        while True:
            if self.debug_objects == False:
                Util.clear_console()
            Util.print_slow('Welcome to the wonderful world of <worldname>! Before you start your adventure, let me ask you who you are.\n\n', False)
            Util.print_slow('Are you a Wandering Cavalier, questing across the realm and smiting evil in the search of glory, wealth, fame, or perhaps all of the above? If so, type "Knight”\n\n', False)
            Util.print_slow('Are you a Traveling Scholar? If so, type “Wizard”\n\n', False)
            Util.print_slow('Are you a Lone Brigand? If so, type “Rogue”\n\n', False)

            for arch in self.player.archetypes: # print list of classes
                print(' *', arch.title()) # print numbered list of node types
            sel = input("\nPlease select which class you would like to play:\n>>> ")
            if sel.lower() == 'knight':
                self.player.archetype = 'knight'
                Util.print_slow("\nYou have chosen Knight, a strong choice!\n\n", False)
            elif sel.lower() == 'wizard':
                self.player.archetype = 'wizard'
                Util.print_slow("\nYou have chosen Wizard, a wise choice!\n\n",  False)
            elif sel.lower() == 'rogue':
                self.player.archetype = 'rogue'
                Util.print_slow("\nYou have chosen Rogue, a dexterous choice!\n\n", False)

            # see if we have a valid choice, break out of while loop if so
            if self.player.archetype != None:
                time.sleep(1)
                if self.debug_objects == False:
                    Util.clear_console()
                break;

            # not a valid choice, loop again
            print("\nPlease enter a valid number!")
            time.sleep(1)

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
        elif sys.argv[2] == "knight" or sys.argv[2] == "wizard" or sys.argv[2] == "rogue":
            state.player.archetype = sys.argv[2]
            print(state.player.archetype)
    if len(sys.argv) > 3:
        state.player.archetype = sys.argv[3]
        print(state.player.archetype)

# load game data dictionaries
state.load_game_data()

# clear console
if state.debug_objects != True:
    Util.clear_console()

# start game loop
while True:

    # see if we need to choose the player type
    if state.player.archetype == None:
        state.prompt_for_archetype()

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

        # check to see if we picked up an item in this node
        val = node.get('item_pickup', None) # e.g. ["stick-lady-map", "potion-of-stomping"]
        if val != None:
            for item in val:
                state.inventory.append(item)

        # check to see if this is an inventory_check node
        val = node.get('inventory_check', None) # e.g. ["stick-lady-map", "potion-of-stomping"]
        if val != None:
            if state.debug_objects == True:
                print(f" * inventory: {state.inventory}")
                print(f" * node item list: {val}")
            if (set(val).issubset(set(state.inventory))):
                val = node['check_success'] # e.g., "id-forest-blah-success",
            else:
                val = node['check_failure'] # e.g., "id-forest-blah-failure",
            state.stateid = val

        # see if this is a goto node
        val = node.get('goto_node', None) # val is either None, string name for next state
        if val != None:
            if val == 'id-game-quit':
                quit()
            elif val == 'id-game-goto-restart':
                state.player.archetype = None
                state.inventory.clear()
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
                Util.print_speed = Util.print_speed_default
            elif action_key == 'faster':
                speed = max(0.00, Util.print_speed - 0.02)
                print(f"ok, new speed: {speed}")
                Util.print_speed = speed
            elif action_key == 'slower':
                speed = min(Util.print_speed_default + 0.02, Util.print_speed + 0.02)
                print(f"ok, new speed: {speed}")
                Util.print_speed = speed
            elif action_key == 'fastest':
                speed = 0.00
                print(f"ok, new speed: {speed}")
                Util.print_speed = speed
            else:
                state.stateid = node[action_key]

            print() #newline

        elif prompt_text != None:

            input("\n" + prompt_text + "\n\n>>> ")


        # see if we need to roll any dice
        roll_data_list = node.get('roll_dice', None) # e.g., [1, 20, 10]
        if roll_data_list != None:

            # get the stat list for this roll
            roll_stat_list = node.get('roll_stats', []) # e.g., ["constitution","strength"]

            # get the item list
            roll_item_list_pairs = node.get('roll_items', []) # e.g., [["good-item", 2], ["bad-item", -4]]

            roll_result = state.roll_dice(roll_data_list, roll_stat_list, roll_item_list_pairs) # e.g., roll_success

            # assign new state id base on that roll result
            state.stateid = node[roll_result]

        if state.debug_objects == True:
            print(f"\n  |Newly assigned node: {state.stateid}|\n")

##########################################################################
##########################################################################
##########################################################################
