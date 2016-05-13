import sys
import os
import shutil
import pickle
from week import *
from category import *

#==================
# CONSTANTS
#==================

DEFAULT_FILENAME = "save.bdat"

INPUT_SPLIT_BY = " "
INPUT_EXIT = "exit"
INPUT_EXIT_SHORT = "x"
INPUT_DISPLAY_ALL = "displayall"
INPUT_NAMES = "names"
INPUT_SET_SAVINGS = "setsavings"
INPUT_PAY = "pay"
INPUT_SAVE = "save"
INPUT_SAVE_SHORT = "s"
INPUT_ADD_CATEGORY = "newcategory"

#===================


def findCategory(name, categories):
    for e in categories:
        if e.name.lower() == name.lower():
            return e
    return None

def parseInstruction(instr, args, categories, openedFilename):

    if instr == INPUT_NAMES:
        for e in categories:
            print(e.name)
        return True

    if instr == INPUT_DISPLAY_ALL:
        weeksback = WEEKS_BACK_STANDARD if args == [] else args[0]
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

    if instr == INPUT_ADD_CATEGORY:
        if len(args) != 2:
            return False
        try: #For number conversion
            nc = Category(args[0], int(args[1]))
        except ValueError:
            return False
        nc.display()
        categories.append(nc)
        return True

    if instr == INPUT_SAVE or instr == INPUT_SAVE_SHORT:
        # Make a backup for the file
        if os.path.isfile(openedFilename):
            try:
                shutil.copyfile(openedFilename, openedFilename + ".bak")
            except OSError:
                print("OS is preventing the program from making a backup. Stopping.")
                return True # Not a syntax error
        # Serializing
        try:
            with open(openedFilename, "wb") as f:
                pickle.dump(categories, f)
        except IOError:
            print("Failed to open file.")
        except pickle.PicklingError:
            print("Serializing failed.")
        return True

    return False


def workOn(categories, openedFilename):

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
        inpArgs = [] if len(inpS) == 1 else inpS[1:]
        
        if inpInstr == INPUT_EXIT or inpInstr == INPUT_EXIT_SHORT:
            return
        else:
             if not parseInstruction(inpInstr, inpArgs, categories, openedFilename):
                 print("Illegal statement.")
             
def main():
    # Opening a saved file
    filename = DEFAULT_FILENAME if len(sys.argv) < 2 else sys.argv[1]
    categories = []
    if os.path.isfile(filename):
        try:
            with open(filename, "rb") as f:
                categories = pickle.load(f)
        except IOError:
            print("File exists, but read permission denied. Exiting.")
            return
        except pickle.PicklingError:
            print("Unable to unserialize file. Exiting.")
            return
    else:
        print(filename, "not found. Creating new file.")
    workOn(categories, filename)
        
if __name__ == "__main__":
    main()
