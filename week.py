class Week:

    remainingMoney = 0
    savings = 0
    maxPerWeek = 0
    number = 0 # Unique identifier
    userModdedSavings = False

    def spend(self, amount):
        if self.remainingMoney > amount:
            self.remainingMoney -= amount
        else:
            dif = amount - self.remainingMoney
            self.remainingMoney = 0
            self.savings -= dif

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

    def setMax(self, amount):
        self.maxPerWeek = amount
        self.increase(0) # Funnels surplus remaining into savings

    def addToSavings(self, amount):
        self.savings += amount

    def userSetSavings(self, amount):
        self.savings = amount
        self.userModdedSavings = True

    def __init__(self, number, maxPerWeek):
        self.remainingMoney = 0
        self.savings = 0
        self.maxPerWeek = maxPerWeek
        self.number = number
