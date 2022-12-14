

from classes.TransactionType import TransactionType


class Transaction():

    def __init__(self, transactionType: TransactionType, quantity: float):
        self.transactionType = transactionType
        self.quantity = str(quantity)
        self.pendingTime = float(self.transactionType.timeOfAttention)*int(quantity)

    def workOneSecond(self):
        self.pendingTime -= (1/60)
