from typing import List
from classes.Transaction import Transaction


class Client():

    def __init__(self, dpi, name, transactions: List[Transaction]):
        self.name = name
        self.dpi = dpi
        self.transactions = transactions
