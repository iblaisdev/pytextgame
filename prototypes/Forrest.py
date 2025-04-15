import random
import time
import sys
import os

nice_to_goblins = False

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
            time.sleep(.04)
    @staticmethod
    def clear_console():
        if (os.name == 'posix'):
            os.system('clear')
        else:
            os.system('cls')

    def __init__(self):
        pass
####################################################################################
    
def forrest():
    Util.print_slow('"You are in the woods at night. You are traveling to a town that has not been heard from for some time."')
    input("\nPress enter to roll for perception\n\n>>> ")  #add slow input?
    result = random.randint(1, 20)
    if result > 5:
        Util.print_slow(f"\nYou rolled a {result}, which succeeds.")
        Util.print_slow('\n"Suddenly, you hear small footsteps ahead. A group is approaching, what do you do?"')
        user_input = input("""\n(Run or Hide)\n\n>>> """)
        print('')
        user_input = user_input.lower()
        if (user_input == 'run'):
            Util.print_slow('''“It appears that your tale will begin somewhere else."
"You escape the woods and find yourself somewhere entirely else and outside the scope of this story."
"If you live in the passing months, you hear that the town in the woods burned down not long after you ran off."
"It makes you wonder, what if you didn’t run away from those goblins in the woods?”''')
            time.sleep(10)
#####################################################################################################################################################################
        elif (user_input == 'hide'):
            Util.print_slow('''"You dash into the brush and find yourself peering at the approaching group from behind a shaded tree."
"A group of seven short, green-skinned humanoid figures sculk past your tree. Goblins, no doubt."
“They don’t see you, and you would have the upper hand in combat if you attack them now."
"But it would still be a tough fight. Maybe it’s best just to let them pass . . .”''')
            user_input = input("""\n(Pass, Talk, or Ambush)\n\n>>> """)
            user_input = user_input.lower()       
            print('')
            if (user_input == 'pass'):
               Util.print_slow('''“You sit back into the brush and listen to the small steps of the goblin troupe get softer as they continue down the forest path. 
You find yourself alone again in the quiet woods, and continue down the trail.”''')
            elif (user_input == 'talk'):
                result = random.randint(1, 20)
                if result > 10:
                    Util.print_slow(f"\nYou rolled a {result}, which succeeds.")
                    Util.print_slow('''“You reveal yourself from the brush, startling the goblins.”
“You come out into the path behind them, and say you are a traveling merchant and friend to goblins.”
“You trade them some small objects and knick-knacks, claiming that they are potent charms and talismans.”
“In return, they give you safe passage through the forest.”
“They also give you the location of a ‘stick lady,’ but they don’t tell you why you would want to visit such a character.”\n
“Soon after they leave. You find yourself alone again in the quiet woods, and continue down the trail.”''')

                else:
                    Util.print_slow(f"\nYou rolled a {result}, which fails.")
                    Util.print_slow('''“You reveal yourself from the brush, startling the goblins.”
“You tell them of your great deeds and many quests that you have completed in the name of good.”
“Being goblins, they don’t care for your great deeds, fictional or not. They kill you.”''')
                    time.sleep(10)
                    
########################################################################################################################################################################
                    
            elif (user_input == 'ambush'):
                result = random.randint(1, 20)
                if result > 10:
                    Util.print_slow(f"\nYou rolled a {result}, which succeeds.")
                    Util.print_slow('''“You follow the band for a short while before silently pulling a goblin into the brush."
“Then a second and a third.”
“The remaining four notice their group is smaller and panic, costing them another member.”
“You then attack head on while the last three goblins are off balance, killing two more. 
“The last one tried to run, but didn’t get far.”''')
                else:
                    Util.print_slow(f"\nYou rolled a {result}, which fails.")
                    Util.print_slow('“You leap out in an attempt to surprise the goblins, only to meet a spear! You are dead.”')

#####################################################################################################################################################################
            else:
                print("Not an answer bub")
        else:
            print("Not an answer bub")      
            
#########################################################3
            
    else:
        Util.print_slow(f"\nYou rolled a {result}, which Fails.")
        Util.print_slow('''\n"But before you could puzzle out what happened to the town, you hear a branch break behind you.”
“An ambush! Short hooded figures emerge from behind the shadowy trees, surrounding you and greeting you with various sharp objects.” 
“Their green skin betrays them as Goblins, and you count at least seven of them. What do you do?"''')
        user_input = input("""\n(Talk or Fight)\n\n>>> """)
        user_input = user_input.lower()       
        print('')
        if (user_input == 'talk'):
            result = random.randint(1, 20)
            if result > 13:
                Util.print_slow(f"You rolled a {result}, which succeeds.")
                Util.print_slow('''\n"There is a tense moment of silence as you struggle to answer their accusations in the few goblin words you know.”
“You manage enough goblinoid through your tongue to convince them you’re a merchant who is friendly to goblins.”
“You trade them some small objects and knick-knacks, claiming that they are potent charms and talismans.”
“In return, they give you safe passage through the forest.”
“They also give you the location of a ‘stick lady,’ but they don’t tell you why you would want to visit such a character.”

“Soon after they leave. You find yourself alone again in the quiet woods, and continue down the trail.”''')
            else:
                Util.print_slow(f"You rolled a {result}, which fails.")
                Util.print_slow('''\n“Unfortunately, you can’t remember anything of the goblin language and are unable to stay their weapons.”
“You die on the road to the village, without so much as a burial to your name.”''')

########################################################################################################################################################################

        elif (user_input == 'fight'):
            result = random.randint(1, 20)
            if result > 10:
                Util.print_slow(f"You rolled a {result}, which succeeds.")
                Util.print_slow('''\n“The largest goblin looks up to you, snarling in its barbaric language, drool dripping from its sharp, uneven teeth.”
“You bash your forehead into the boss goblin’s noggin before severing it from the rest of its body. ”
“Next are the two goblins behind you, which are dealt with easily in their surprise. You carve a path through the group.”
“With the extra distance between you and the group, you kill the goblins as they reach you, one by one.”
“In the end, you are coated in goblin blood with six dead around you.”
“The boss, reeling from his head wound, screams in pain and begs for mercy. He does not receive any from you.”

“You find yourself alone again in the quiet woods, and continue down the trail.”''')
            else:
                Util.print_slow(f"You rolled a {result}, which fails.")
                Util.print_slow('''\n“The largest goblin looks up to you, snarling in its barbaric language, drool dripping from its sharp, uneven teeth.”
“You attempt to bash your head into the boss goblin, but he predicts your movement, dodging at the last moment.”
“The goblins, enraged, ready their spears and attack. You are dead.”''')

        else:
            print('Not an answer bub')

##########################################################################################################
        
forrest()
time.sleep(30)