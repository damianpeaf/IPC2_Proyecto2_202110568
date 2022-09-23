

from classes.TransactionType import TransactionType


class Transaction():

    def __init__(self, transactionType: TransactionType, quantity: float):
        self.transactionType = transactionType
        self.quantity = quantity
