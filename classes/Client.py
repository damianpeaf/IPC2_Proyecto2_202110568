from classes.Transaction import Transaction
from core.SimpleList import SimpleList


class Client():

    def __init__(self, dpi, name):
        self.name = name
        self.dpi = dpi
        self.transactions = SimpleList[Transaction]()
        self.waitedTime = 0

    def waitOneSecond(self):
        self.waitedTime += (1/60)
