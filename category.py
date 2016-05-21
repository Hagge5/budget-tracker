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

# Expands or shrinks a string to make it the desired length.
# Does not modify given strings, merely returns the expanded/shrunken version.
# fillChar is the char to fill it out with, " " is usually desired.
# Returns the expanded/shrunken string.
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

# Helper function for printing table elements; a special case of asLength(...).
# Cell width is determined by global constant DISPLAY_COLUMN_WIDTH.
# If divisor==True, a vertical seperator is added at the end of the output.
# Returns None, merely prints the result
def printColumnElement(string, divisor):
    print(asLength(string, DISPLAY_COLUMN_WIDTH, True, " "), end="")
    if divisor:
        print("|", end="")

# Returns the current week number, sundays being the start of a new week.
def currentWeek():
    today = datetime.today()
    return 1 + int(today.strftime("%U"))

# Returns the current year number.
def currentYear():
    today = datetime.today()
    return 1 + today.year

# Returns a unique number for the current week.
# A currentWeek() result repeats once per year, this does not.
def currentUniqueWeek():
    return currentWeek() + WEEKS_PER_YEAR * currentYear()

# A spending Category; e.g "Rent", "Food", et.c.
class Category:
    name = ""
    weeks = []
    moneyPerWeek = 0

    # Prints a table of each weeks spending.
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

    # Returns the newest Week the category is tracking.
    def thisWeek(self):
        return self.weeks[-1]
    
    # Adds a new week to the category if the newest 
    #   week being tracked is a past week.
    # Returns True if one was added, False if not.
    def newWeek(self):
        if self.weeks != [] and self.thisWeek().number == currentUniqueWeek():
            return False
        new = Week(currentUniqueWeek(), self.moneyPerWeek)
        if self.weeks != []:
            new.addToSavings(self.thisWeek().savings + self.thisWeek().remainingMoney)
        new.increase(self.moneyPerWeek)
        self.weeks.append(new)
        return True
    
    # Modified behaviour to support
    #   Serializing of the "weeks" member
    def __getstate__(self):
        dcpy = self.__dict__.copy()
        dweeks = {"weeks": self.weeks}
        dcpy.update(dweeks)
        return dcpy
    
    # Constructor.
    def __init__(self, name, maxMoneyPerWeek):
        self.name = name
        self.moneyPerWeek = maxMoneyPerWeek
        self.weeks = []
        self.newWeek()
