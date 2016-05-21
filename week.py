
# Keeps track of spending over the course of a week
class Week:

    remainingMoney = 0
    savings = 0
    maxPerWeek = 0
    number = 0 # Unique identifier
    userModdedSavings = False

    # Spend some money, lowering remaining money,
    #   updating savings accordingly
    def spend(self, amount):
        if self.remainingMoney > amount:
            self.remainingMoney -= amount
        else:
            dif = amount - self.remainingMoney
            self.remainingMoney = 0
            self.savings -= dif

    # Increase the remaining money.
    # If remaining exceeds max per week, surplus is funneled to savings.
    # If savings is below 0, savings will receive funds before remaining money.
    def increase(self, amount):
        self.remainingMoney += amount
        # We prioritize having savings above 0 over this weeks money
        if self.savings < 0:
            if self.remainingMoney > abs(self.savings):
                self.remainingMoney += self.savings
                self.savings = 0
            else:
                self.savings += self.remainingMoney
                self.remainingMoney = 0
        # If we have surplus money, funnel it to savings
        if self.remainingMoney > self.maxPerWeek:
            self.savings += self.remainingMoney - self.maxPerWeek
            self.remainingMoney = self.maxPerWeek

    # Sets the max amount of money spendable.
    # Max amount determines when surplus is transfered to savings.
    # Updates savings accordingly.
    def setMax(self, amount):
        self.maxPerWeek = amount
        self.increase(0) # Funnels surplus remaining into savings

    # Adds money to savings.
    def addToSavings(self, amount):
        self.savings += amount

    # Adds money to savings, but changes a flag to record this event.
    # Meant to be called as user demands it, thus tracking his actions.
    def userSetSavings(self, amount):
        self.savings = amount
        self.userModdedSavings = True

    # Constructor.
    def __init__(self, number, maxPerWeek):
        self.remainingMoney = 0
        self.savings = 0
        self.maxPerWeek = maxPerWeek
        self.number = number
