import json
import time
import sys
import os

##########################################################################
class Util:

    @staticmethod
    def __init__():
        pass

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
        self.regiondata = {}
        self.region_name = None             # e.g., "forest.json
        self.incomplete_node_list = []    # list of lists - e.g., ['id-forest-footsteps-run', '{id-forest-footsteps': "..."], aka, [child-name, parent-node]
        self.node_types = ['goto_node', 'dieroll_node', 'user_input_node', 'inventory_check', 'done']

    def save_region_data(self):
        self.gamedata = {} # {"id-game-start" : {"prompt_text": "(Run or pass)","parse_input": ["run", "pass"], "run" : "id-forest-start", "pass" : "id-forest-blah"}}
        with open(self.region_name + ".json", "w") as json_file:
            json.dump(self.regiondata, json_file, ensure_ascii=True, indent=4)

    def read_intro_text_list(self, nodename):
        txt = input(f"\n(OPTIONAL) Enter 'intro_text' for node '{nodename}'. Use '@' to seperate entries:\n\n>>> ")
        if len(txt) > 2:
            return txt.split('@')
        return None

    def read_space_separated_list(self, prompt):
        txt = input(prompt)
        if len(txt) > 2:
            return txt.split(' ')
        return None

    def print_node(self, node):
        print()
        print('*' * 120)
        print(f"NODE_PARENT: {node}")
        print('*' * 120)

    def prompt_for_new_node_type(self): # returns e.g., 'dieroll_node'
        while True:
            for number, ntype in enumerate(self.node_types):
                print(number + 1, ntype) # print numbered list of node types
            sel = input("\nSelect the next node type:\n\n>>> ")
            try:
                if int(sel) > 0:
                    idx = int(sel)-1
                    self.node_types[idx] # throws exception if not found
                    return self.node_types[idx]
            except (IndexError, ValueError) as e:
                pass
            print("Not a valid index")
            time.sleep(1)


##########################################################################
##########################################################################
##########################################################################

# create state
state = State()

# clear console
Util.clear_console()

# start game loop
while True:

    if state.region_name == None:
        state.region_name = input("Enter region name (e.g. 'forest'):\n\n>>> ")

    '''
    "id-forest-start" : {
        "intro_text" : ["You are in the woods at night..."],
        "goto_node" : "id-forest-at-night"
    },
    '''
    # special case: if no current node, create the first one of region
    if not state.regiondata:
        targetname = f"id-{state.region_name}-start"
        node = {"goto_node":""}
        intro_text_list = state.read_intro_text_list(targetname)
        if intro_text_list != None:
            node['intro_text'] = intro_text_list
        state.regiondata[targetname] = node
        state.incomplete_node_list.append([targetname, "goto_node", {}]) #aka, [parent-name, parent-child-key, parent-node]

    # if we have no more in list to work on, we're done'
    if not state.incomplete_node_list:
        print("\n\nEnd of incomplete_node_list... region complete!")
        break # leave while loop

    # choose front node from incomplete_node_list to work on
    node_data_list = state.incomplete_node_list.pop(0)  #aka, [parent-name, parent-child-key, parent-node]
    active_node_name = node_data_list[0]                #aka, 'id-forest-footsteps'
    active_parent_child_key = node_data_list[1]         #aka, 'roll_success' or 'goto_node'

    #print(f"\n * active_parent_child_key: {active_parent_child_key}")
    #print(f" * current regiondata: {state.regiondata}")

    # print the current node parent we're working on
    state.print_node(node_data_list[2])

    print(f"\n * ACTIVE NODE: {active_node_name}\n")

    #get the next node
    print(f"Select target node for the '{active_parent_child_key}' of '{active_node_name}'")
    newtype = state.prompt_for_new_node_type()
    print(f"you selected: {newtype}\n") #['goto_node', 'dieroll_node', 'user_input_node', 'inventory_check', 'done']

    # see if selected node is a goto_node
    if newtype == 'goto_node':

        #get the next node
        targetname = input(f"(REQUIRED) Enter name for new goto_node (id-{state.region_name}-xxxx-xxxx)\n\n>>> ")

        #get intro strings for goto node
        intro_text_list = state.read_intro_text_list(targetname)

        #hookup parent node to this one
        state.regiondata[active_node_name][active_parent_child_key] = targetname

        #create a new node
        node = { 'goto_node' : {} }
        if intro_text_list:
            node['intro_text'] = intro_text_list

        # see if there is an item pickup for this node
        itemlist = input(f"\n(OPTIONAL) Enter any item_pickup for '{targetname}', seperated with spaces. Leave blank for none. EXAMPLE: stick-lady-map another-item\n\n>>> ")
        if itemlist:
            node['item_pickup'] = []
            for item in itemlist.split(' '):
                elem = item.replace("'", "").strip('"') #no single or double quotes
            node['item_pickup'].append(elem)

        #add this new goto node to regiondata
        state.regiondata[targetname] = node

        #queue up the goto target for next work
        state.incomplete_node_list.append([targetname, 'goto_node', node]) #aka, [targetname, active_parent_child_key, parent-node]

    elif newtype == 'dieroll_node':

        #get the next node
        targetname = input(f"(REQUIRED) Enter name for new dieroll_node (id-{state.region_name}-xxxx-xxxx)\n\n>>> ")

        #hookup parent node to this one
        state.regiondata[active_node_name][active_parent_child_key] = targetname

        #create new node
        node = { 'roll_success' : {}, 'roll_failure' : {} }

        #get intro strings for this node
        intro_text_list = state.read_intro_text_list(targetname)
        if intro_text_list:
            node['intro_text'] = intro_text_list
        
        #get prompt text
        prompt_text = input(f"\n(OPTIONAL) Enter prompt text for die roll, leave blank for none.\n\n>>> ")
        if prompt_text:
            node['prompt_text'] = prompt_text

        #get roll info
        roll_dice = input(f"\n(REQUIRED) Enter the dice roll values for '{targetname}', seperated with spaces. EXAMPLE: 1 20 10\n\n>>> ")
        roll_dice = roll_dice.replace("'", "").strip('"') #no single or double quotes
        while roll_dice and len(roll_dice) == 3:
            node['roll_dice'] = [int(roll_dice[0]), int(roll_dice[1]), int(roll_dice[2])]

        #get roll stats
        prompt = f"\n(OPTIONAL) Enter roll_stat modifiers for node '{targetname}'. Use SPACE to seperate entries. EXAMPLE: wisdom wisdom charisma:\n\n>>> "
        roll_stats = state.read_space_separated_list(prompt)
        if roll_stats:
            node['roll_stats'] = [roll_stats]

        # see if there is an item pickup for this node
        itemlist = input(f"\n(OPTIONAL) Enter any item_pickup for '{targetname}', seperated with spaces. Leave blank for none. EXAMPLE: stick-lady-map another-item\n\n>>> ")
        if itemlist:
            node['item_pickup'] = []
            for item in itemlist.split(' '):
                elem = item.replace("'", "").strip('"') #no single or double quotes
            node['item_pickup'].append(elem)

        #get roll itmes
        print("\n#################### BEGIN item roll modifier entries ####################")
        roll_items_list_list = []
        prompt = f"\n(OPTIONAL) Enter ONE roll_item name and modifier for node '{targetname}'. Use SPACE to seperate entries. EXAMPLE: example-item 2:\n\n>>> "
        roll_items = state.read_space_separated_list(prompt)
        while roll_items and len(roll_items) == 2:
            roll_items_list_list.append([roll_items[0], int(roll_items[1])])
            roll_items = state.read_space_separated_list(prompt)
        if (roll_items_list_list != None):
            node['roll_items'] = roll_items_list_list
        print("\n#################### END item roll modifier entries ####################\n")

        #add this new goto node to regiondata
        state.regiondata[targetname] = node

        #queue up the roll_success target for next work
        state.incomplete_node_list.append([targetname, 'roll_success', node]) #aka, [targetname, active_parent_child_key, parent-node]

        #queue up the roll_failure target for next work
        state.incomplete_node_list.append([targetname, 'roll_failure', node]) #aka, [targetname, active_parent_child_key, parent-node]


    elif newtype == 'user_input_node':

        #get the next node
        targetname = input(f"(REQUIRED) Enter name for new user_input_node (id-{state.region_name}-xxxx-xxxx)\n\n>>> ")

        #hookup parent node to this one
        state.regiondata[active_node_name][active_parent_child_key] = targetname

        #create new node
        node = { }

        #get intro strings for this node
        intro_text_list = state.read_intro_text_list(targetname)
        if intro_text_list:
            node['intro_text'] = intro_text_list

        #get prompt text
        prompt_text = input(f"\n(REQUIRED) Enter prompt text to ask user. EXAMPLE: (Talk or Fight)\n\n>>> ")
        node['prompt_text'] = prompt_text

        #get allowed input
        prompt_text = input(f"\n(REQUIRED) Enter allowed input list, seperated with spaces. EXAMPLE: talk fight\n\n>>> ")
        allowed_input_list = prompt_text.split(' ')
        node['parse_input'] = allowed_input_list

        # see if there is an item pickup for this node
        itemlist = input(f"\n(OPTIONAL) Enter any item_pickup for '{targetname}', seperated with spaces. Leave blank for none. EXAMPLE: stick-lady-map another-item\n\n>>> ")
        if itemlist:
            node['item_pickup'] = []
            for item in itemlist.split(' '):
                elem = item.replace("'", "").strip('"') #no single or double quotes
            node['item_pickup'].append(elem)

        #add this new goto node to regiondata
        state.regiondata[targetname] = node

        #queue each possible input target
        for el in allowed_input_list:

            #queue up the allowed_input target for next work
            state.incomplete_node_list.append([targetname, el, node]) #aka, [targetname, allowed_input, parent-node]

    elif newtype == 'inventory_check':

        #get the next node
        targetname = input(f"(REQUIRED) Enter name for new inventory_check node (id-{state.region_name}-xxxx-xxxx)\n\n>>> ")

        #hookup parent node to this one
        state.regiondata[active_node_name][active_parent_child_key] = targetname

        #get intro strings for goto node
        intro_text_list = state.read_intro_text_list(targetname)

        #get item check info
        check_list = input(f"\n(REQUIRED) Enter each item name for inventory_check for '{active_node_name}', seperated with spaces. EXAMPLE: my-item-name another-item-name\n\n>>> ")
        check_list = check_list.replace("'", "").strip('"') #no single or double quotes

        #add this new goto node to regiondata
        node = { 'inventory_check' : check_list.split(' ') }
        if intro_text_list:
            node['intro_text'] = intro_text_list
        state.regiondata[targetname] = node

        #queue up the check_success target for next work
        state.incomplete_node_list.append([targetname, 'check_success', node]) #aka, [targetname, active_parent_child_key, parent-node]

        #queue up the check_failure target for next work
        state.incomplete_node_list.append([targetname, 'check_failure', node]) #aka, [targetname, active_parent_child_key, parent-node]

    elif newtype == 'done':

        #link end node
        targetname = input(f"\n(REQUIRED) Enter the [LEAF] node target-name for the '{active_parent_child_key}' entry of node '{active_node_name}' (e.g., id-<new_area> or id-game-end)\n\n>>> ")

        #hookup parent node to this one
        #print(f"\n * parent: {active_node_name}")
        #print(f" * active_parent_child_key: {active_parent_child_key}")
        #print(f" * curretnt regiondata: {state.regiondata}")
        state.regiondata[active_node_name][active_parent_child_key] = targetname


# save this region data to json
state.save_region_data()

##########################################################################
##########################################################################
##########################################################################
