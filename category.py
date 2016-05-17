from datetime import *
from week import *

#==================
# CONSTANTS
#==================

DISPLAY_WIDTH = 48
DISPLAY_COLUMN_WIDTH = 12

WEEKS_PER_YEAR = 52

WEEKS_BACK_STANDARD = 8

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
            smodChar = "*" if week.userModdedSavings else ""
            printColumnElement(smodChar + str(week.savings), False)
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
    
    def __getstate__(self):
        # Modified behaviour to support
        # Serializing of the "weeks" member
        dcpy = self.__dict__.copy()
        dweeks = {"weeks": self.weeks}
        dcpy.update(dweeks)
        return dcpy
    
    def __init__(self, name, maxMoneyPerWeek):
        self.name = name
        self.moneyPerWeek = maxMoneyPerWeek
        self.weeks = []
        self.newWeek()
