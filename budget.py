import sys
from datetime import *

#==================
# CONSTANTS
#==================

DISPLAY_WIDTH = 48
DISPLAY_COLUMN_WIDTH = 12

WEEKS_PER_YEAR = 52

WEEKS_BACK_STANDARD = 8

INPUT_SPLIT_BY = " "
INPUT_EXIT = "exit"
INPUT_EXIT_SHORT = "x"
INPUT_DISPLAY_ALL = "displayall"
INPUT_NAMES = "names"
INPUT_PAY = "pay"

#===================


def asLength(string, desiredLength, fillBehind, fillChar):
    result = string
    while len(result) > desiredLength:
        result = result[:len(result)-1]
    while len(result) < desiredLength:
        if fillBehind:
            result += fillChar
        else:
            result = fillChar + result
    return result

def printColumnElement(string, divisor):
    print(asLength(string, DISPLAY_COLUMN_WIDTH, True, " "), end="")
    if divisor:
        print("|", end="")

def currentWeek():
    today = datetime.today()
    return 1 + int(today.strftime("%U"))

def currentYear():
    today = datetime.today()
    return 1 + today.year

def currentUniqueWeek():
    return currentWeek() + WEEKS_PER_YEAR * currentYear()

class Week:

    remainingMoney = 0
    savings = 0
    maxPerWeek = 0
    number = 0 # Unique identifier

    def spend(self, amount):
        if self.remainingMoney > amount:
            self.remainingMoney -= amount
        else:
            dif = amount - self.remainingMoney
            self.remainingMoney = 0
            self.savings -= dif

    def increase(self, amount):
        self.remainingMoney += amount
        if self.remainingMoney > self.maxPerWeek:
            self.savings += self.remainingMoney - self.maxPerWeek
            self.remainingMoney = self.maxPerWeek

    def setMax(self, amount):
        self.maxPerWeek = amount
        self.increase(0) # Funnels surplus remaining into savings

    def addToSavings(self, amount):
        self.savings += amount

    def __init__(self, number, maxPerWeek):
        self.remainingMoney = 0
        self.savings = 0
        self.maxPerWeek = maxPerWeek
        self.number = number

class Category:
    name = ""
    weeks = []
    moneyPerWeek = 0

    def display(self, weeksBack = WEEKS_BACK_STANDARD):
        print('-' * (len(self.name)+2))
        print(self.name + " |")
        print('-' * DISPLAY_WIDTH)
        printColumnElement("Week", True)
        printColumnElement("$/week", False)
        printColumnElement("Remaining", False)
        printColumnElement("Savings", False)
        print("\n" + '-' * DISPLAY_WIDTH, end="")
        for week in self.weeks:
            print("")
            if week.number < currentUniqueWeek() - weeksBack:
                continue
            printColumnElement("w" + str(week.number % WEEKS_PER_YEAR), True)
            printColumnElement(str(week.maxPerWeek), False)
            printColumnElement(str(week.remainingMoney), False)
            printColumnElement(str(week.savings), False)
        print("\n" + '-' * DISPLAY_WIDTH)
        
    def thisWeek(self):
        return self.weeks[-1]
    
    def newWeek(self):
        if self.weeks != [] and self.thisWeek().number == currentUniqueWeek():
            return False
        new = Week(currentUniqueWeek(), self.moneyPerWeek)
        new.increase(self.moneyPerWeek)
        if self.weeks != []:
            new.addToSavings(self.thisWeek().savings + self.thisWeek().remainingMoney)
        self.weeks.append(new)
        return True
    
    def __init__(self, name, maxMoneyPerWeek):
        self.name = name
        self.moneyPerWeek = maxMoneyPerWeek
        self.newWeek()


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
