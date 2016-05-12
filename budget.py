import sys
from week import *
from category import *

#==================
# CONSTANTS
#==================

INPUT_SPLIT_BY = " "
INPUT_EXIT = "exit"
INPUT_EXIT_SHORT = "x"
INPUT_DISPLAY_ALL = "displayall"
INPUT_NAMES = "names"
INPUT_SET_SAVINGS = "setsavings"
INPUT_PAY = "pay"

#===================


def findCategory(name, categories):
    for e in categories:
        if e.name.lower() == name.lower():
            return e
    return None

def parseInstruction(instr, args, categories):

    if instr == INPUT_NAMES:
        for e in categories:
            print(e.name)
        return True

    if instr == INPUT_DISPLAY_ALL:
        weeksback = WEEKS_BACK_STANDARD if args is None else args[0]
        for e in categories:
            e.display(weeksback)
        return True

    if instr == INPUT_PAY:
        if len(args) != 2:
            return False
        cat = findCategory(args[0], categories)
        if cat is None:
            return False
        try: # For conversion to work
            cat.thisWeek().spend(int(args[1]))
        except ValueError:
            return False
        cat.display()
        return True

    if instr == INPUT_SET_SAVINGS:
        if len(args) != 2:
            return False
        cat = findCategory(args[0], categories)
        if cat is None:
            return False
        try: # For conversion to work
            cat.thisWeek().userSetSavings(int(args[1]))
        except ValueError:
            return False
        cat.display()
        return True


    return False


def workOn(categories):

    # Update weeks
    for e in categories:
        # Adds a new week if no entry exists
        if e.newWeek():
            print("Added a week to", e.name)

    while True:
        
        print(">", end="")
        inp = input().lower()
        inpS = inp.split(INPUT_SPLIT_BY)
        inpInstr = inpS[0]
        inpArgs = None if len(inpS) == 1 else inpS[1:]
        
        if inpInstr == INPUT_EXIT or inpInstr == INPUT_EXIT_SHORT:
            return
        else:
             if not parseInstruction(inpInstr, inpArgs, categories):
                 print("Illegal statement.")
             
        
        

o = Category("Food", 450)
p = Category("Fun", 90)

workOn([o])
