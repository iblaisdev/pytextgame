import random
import json
import time
import sys
import os

##########################################################################
class Util:

    print_speed_default = .03
    print_speed_override = -1.0
    print_speed = .03

    @staticmethod
    def __init__():
        pass

    @staticmethod
    def print_slow(s: str, addquotes: bool):

        if s == "":
            print()
            return

        speed = Util.print_speed
        if float(Util.print_speed_override) >= 0.0:
            speed = float(Util.print_speed_override)
            Util.print_speed_override = -1.0

        if addquotes == True:
            print("    \"", end='')

        for letter in s:
            print(letter, end='')
            sys.stdout.flush()
            if speed > 0.0:
                time.sleep(speed)

        if addquotes == True:
            print("\"")
        Util.print_next_one_fastest = False

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

    def get_stat_roll_modifier(self, roll_stat_list_pairs):
        mod = 0
        for stat_pair in roll_stat_list_pairs: #e.g. ["constitution","strength"]
            if stat_pair[0] == 'constitution' and self.archetype == 'knight':
                mod += stat_pair[1]
            if stat_pair[0] == 'strength' and self.archetype == 'knight':
                mod += stat_pair[1]
            if stat_pair[0] == 'intelligence' and self.archetype == 'wizard':
                mod += stat_pair[1]
            if stat_pair[0] == 'wisdom' and self.archetype == 'wizard':
                mod += stat_pair[1]
            if stat_pair[0] == 'dexterity' and self.archetype == 'rogue':
                mod += stat_pair[1]
            if stat_pair[0] == 'charisma' and self.archetype == 'rogue':
                mod += stat_pair[1]
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
        with open('resources/game.json') as json_file:
            self.gamedata = json.load(json_file)
        with open('resources/forest.json') as json_file:
            self.gamedata.update(json.load(json_file))
        with open('resources/town.json') as json_file:
            self.gamedata.update(json.load(json_file))
        with open('resources/gobden.json') as json_file:
            self.gamedata.update(json.load(json_file))
        with open('resources/crypt.json') as json_file:
            self.gamedata.update(json.load(json_file))
        with open('resources/witch.json') as json_file:
            self.gamedata.update(json.load(json_file))
        with open('resources/dragon.json') as json_file:
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

    def roll_dice(self, roll_data_list, roll_stat_list_pairs, roll_item_list_pairs):

        minval = roll_data_list[0] # e.g., 1
        maxval = roll_data_list[1] # e.g., 20
        chkval = roll_data_list[2] # e.g., 13
        result = random.randint(minval, maxval)
        statmod = self.player.get_stat_roll_modifier(roll_stat_list_pairs)
        itemmod = self.get_item_roll_modifier(roll_item_list_pairs)
        result += statmod + itemmod
        sign = '+' if itemmod >= 0 else '-'
        itemmod = abs(itemmod)
        if result > chkval:
            if not roll_item_list_pairs:
                Util.print_slow(f"\nYou rolled {result} (+{statmod} class), which succeeds.\n\n", False)
            else:
                Util.print_slow(f"\nYou rolled {result} (+{statmod} class, {sign}{itemmod} items), which succeeds.\n\n", False)
            return 'roll_success'
        else:
            if not roll_item_list_pairs:
                Util.print_slow(f"\nYou rolled {result} (+{statmod} class), which fails.\n\n", False)
            else:
                Util.print_slow(f"\nYou rolled {result} (+{statmod} class, {sign}{itemmod} items), which fails.\n\n", False)
            return 'roll_failure'

    def process_input(self, prompt_text: str, allowed_actions, loop_until_true: bool):
        while True:
            user_entered_txt = input("\n" + prompt_text + "\n\n>>> ")
            clean_input = self.__sanitize_input(user_entered_txt)
            if self.debug_objects == True:
                print(f"user_entered_txt: {user_entered_txt}\nclean_input: {clean_input}")
            for action in allowed_actions:
                if action == clean_input:
                    return action # e.g., 'run'
            if not loop_until_true:
                return "fail"
            if clean_input != "settingschange":
                print('Not an answer bub')

    # parse user input to allowed values
    def __sanitize_input(self, user_input: str):
        txt = user_input.lower()
        if self.debug_objects == True:
            print(f"txt: {txt}")
        if "knight" in txt:
            return "knight"
        if "wizard" in txt:
            return "wizard"
        if "rogue" in txt:
            return "rogue"
        if "talk" in txt:
            return "talk"
        if "fight" in txt:
            return "fight"
        if "run" in txt:
            return "run"
        if "ambush" in txt:
            return "ambush"
        if "yes" in txt:
            return "yes"
        if "no" in txt:
            return "no"
        if "enter" in txt:
            return "enter"
        if "leave" in txt:
            return "leave"
        if "pass" in txt:
            return "pass"
        if "hide" in txt:
            return "hide"
        if "steel" in txt:
            return "steel thyself"
        if "crypt" in txt:
            return "the crypt"
        if "goblin" in txt:
            return "the goblin den"
        if "witch" in txt:
            return "the witch hut"
        if "dragon" in txt:
            return "the dragons den"
        if "faster" in txt:
            speed = max(0.00, Util.print_speed - 0.01)
            print(f"ok, new speed: {speed}")
            Util.print_speed = speed
            return "settingschange"
        if "fastest" in txt:
            speed = 0.00
            print(f"ok, new speed: {speed}")
            Util.print_speed = speed
            return "settingschange"
        if "slower" in txt:
            speed = min(Util.print_speed_default + 0.01, Util.print_speed + 0.01)
            print(f"ok, new speed: {speed}")
            Util.print_speed = speed
            return "settingschange"
        if "restart" in txt:
            state.stateid = 'id-game-restart'
            Util.print_speed = Util.print_speed_default
            return "settingschange"
        if "debugobj" in txt:
            self.set_debug_objects(True)
            return "settingschange"
        if "debugtime" in txt:
            self.set_debug_time(True)
            return "settingschange"
        if "ndebug" in txt:
            self.set_debug_objects(False)
            self.set_debug_time(False)
            return "settingschange"
        return "fail" #not valid

    # ask user what class they want to play
    def prompt_for_archetype(self):
        if self.debug_objects == False:
            Util.clear_console()

        Util.print_slow('Welcome to the wonderful world of Gaireabour! Before you start your adventure, let me ask you who you are.\n\n', False)
        Util.print_slow('Are you a Wandering Cavalier, questing across the realm and smiting evil in the search of glory, wealth, fame, or perhaps all of the above? If so, type "Knight”\n\n', False)
        Util.print_slow('Are you a Traveling Scholar? If so, type “Wizard”\n\n', False)
        Util.print_slow('Are you a Lone Brigand? If so, type “Rogue”\n\n', False)

        while True:
            for arch in self.player.archetypes: # print list of classes
                print(' *', arch.title()) # print numbered list of node types
            sel = state.process_input("Please enter which class you would like to play:", ["knight", "wizard", "rogue"], False)
            if sel == 'knight':
                self.player.archetype = 'knight'
                Util.print_slow("\nYou have chosen Knight, a strong choice!\n\n", False)
            elif sel == 'wizard':
                self.player.archetype = 'wizard'
                Util.print_slow("\nYou have chosen Wizard, a wise choice!\n\n",  False)
            elif sel == 'rogue':
                self.player.archetype = 'rogue'
                Util.print_slow("\nYou have chosen Rogue, a dexterous choice!\n\n", False)

            # see if we have a valid choice, break out of while loop if so
            if self.player.archetype != None:
                time.sleep(1)
                if self.debug_objects == False:
                    Util.clear_console()
                break;

            # not a valid choice, loop again
            print("\nPlease enter a valid option!\n")
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

        #see if we have a print speed override
        speed_override = -1.0
        val = node.get('print_speed', None) # val is either None, or a list of strings
        if val != None:
            speed_override = float(val)

        # print intro text for this event
        val = node.get('intro_text', None) # val is either None, or a list of strings
        if val != None:
            for entry in val:
                Util.print_speed_override = speed_override
                Util.print_slow(entry, True)

        # check to see if we picked up an item in this node
        val = node.get('item_pickup', None) # e.g. ["stick-lady-map", "vitality-potion"]
        if val != None:
            for item in val:
                state.inventory.append(item)

        # check to see if we removed an item in this node
        val = node.get('item_remove', None) # e.g. ["vitality-potion", "someother-item"]
        if val != None:
            if state.debug_objects == True:
                print(f"  | inventory before remove: {state.inventory}")
            state.inventory = [e for e in state.inventory if e not in val]
            if state.debug_objects == True:
                print(f"  | inventory after remove: {state.inventory}")

        # check to see if this is an inventory_check node
        val = node.get('inventory_check', None) # e.g. ["stick-lady-map", "vitality-potion"]
        if val != None:
            if state.debug_objects == True:
                print(f" * inventory: {state.inventory}")
                print(f" * node item list: {val}")
            if (set(val).issubset(set(state.inventory))):
                val = node['check_success'] # e.g., "id-forest-blah-success",
            else:
                val = node['check_failure'] # e.g., "id-forest-blah-failure",
            state.stateid = val

        # check to see if this is a class_check node
        val = node.get('class_check', None) # e.g. ["knight", "rogue"]
        if val != None:
            if state.player.archetype in val:
                val = node['check_success'] # e.g., "id-forest-blah-success",
            else:
                val = node['check_failure'] # e.g., "id-forest-blah-failure",
            state.stateid = val
            if state.debug_objects == True:
                print(f"  | class check: new node: {state.stateid}")

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
            action_key = state.process_input(prompt_text, parse_input, True) # e.g. 'run'

            # assign new state id base on that node key, but allow 'restart' always
            if action_key == 'restart':
                state.stateid = 'id-game-restart'
                Util.print_speed = Util.print_speed_default
            elif action_key == 'faster':
                speed = max(0.00, Util.print_speed - 0.01)
                print(f"ok, new speed: {speed}")
                Util.print_speed = speed
            elif action_key == 'slower':
                speed = min(Util.print_speed_default + 0.01, Util.print_speed + 0.01)
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
            roll_stat_list_pairs = node.get('roll_stats', []) # e.g., [["constitution" 4], ["strength" 2]]

            # get the item list
            roll_item_list_pairs = node.get('roll_items', []) # e.g., [["good-item", 2], ["bad-item", -4]]

            roll_result = state.roll_dice(roll_data_list, roll_stat_list_pairs, roll_item_list_pairs) # e.g., roll_success

            # assign new state id base on that roll result
            state.stateid = node[roll_result]

        if state.debug_objects == True:
            print(f"\n  |Newly assigned node: {state.stateid}|\n")

##########################################################################
##########################################################################
##########################################################################
