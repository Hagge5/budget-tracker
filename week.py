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
