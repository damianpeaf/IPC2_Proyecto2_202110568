from typing import List
from classes.Transaction import Transaction


class Client():

    def __init__(self, name, dpi, transactions: List[Transaction]):
        self.name = name
        self.dpi = dpi
        self.transactions = transactions
