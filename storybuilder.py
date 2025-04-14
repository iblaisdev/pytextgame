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

    def read_intro_text_list(self, targetname):
        txt = input(f"Enter intro text for {targetname}. Use '@' to seperate entries:\n\n>>> ")
        if len(txt) > 2:
            return txt.split('@')
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
        node_name = f"id-{state.region_name}-start"
        node = {"goto_node":""}
        strlist = state.read_intro_text_list(node_name)
        if strlist != None:
            node['intro_text'] = strlist
        state.regiondata[node_name] = node
        state.incomplete_node_list.append([node_name, "goto_node", {}]) #aka, [parent-name, parent-child-key, parent-node]

    # if we have no more in list to work on, we're done'
    if not state.incomplete_node_list:
        print("End of incomplete_node_list... region complete!")
        break # leave while loop

    # choose front node from incomplete_node_list to work on
    node_data_list = state.incomplete_node_list.pop(0) #aka, [parent-name, parent-child-key, parent-node]
    parent_name = node_data_list[0]
    parent_child_key = node_data_list[1]

    # print the current node parent we're working on
    state.print_node(node_data_list[2])

    #get the next node
    print(f"Select target node for the {parent_child_key} link for node: {parent_name}")
    newtype = state.prompt_for_new_node_type()
    print(f"you selected: {newtype}") #['goto_node', 'dieroll_node', 'user_input_node', 'inventory_check', 'done']

    # see if selected node is a goto_node
    if newtype == 'goto_node':

        #get the next node
        targetname = input(f"enter target node name for this goto (id-{state.region_name}-xxxx-xxxx)\n\n>>> ")

        #hookup parent node to this one
        print(f"parent: {parent_name}")
        print(f"parent_child_key: {parent_child_key}")
        print(f"state.regiondata: {state.regiondata}")
        state.regiondata[parent_name][parent_child_key] = targetname

        #get intro strings for this goto
        strlist = state.read_intro_text_list(targetname)

        #add this new goto node to regiondata
        node = { "intro_text" : strlist, 'goto_node' : targetname }
        state.regiondata[targetname] = node

        #queue up the goto target for next work
        state.incomplete_node_list.append([parent_name, parent_child_key, node]) #aka, [parent-name, parent-child-key, parent-node]

    elif newtype == 'dieroll_node':
        pass

    elif newtype == 'user_input_node':
        pass

    elif newtype == 'inventory_check':
        pass

    elif newtype == 'done':
        print("Done selected... region complete!")
        break # leave while loop

# save region data to json
state.save_region_data()

##########################################################################
##########################################################################
##########################################################################
