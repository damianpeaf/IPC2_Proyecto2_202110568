
from typing import List
from classes.AttentionPoint import AttentionPoint
from classes.TransactionType import TransactionType


class Company():

    def __init__(self, id, name: str, abbreviaton: str, atentionPoints: List[AttentionPoint], availableTransactions: List[TransactionType]):
        self.id = id
        self.name = name
        self.abbreviaton = abbreviaton
        self.attentionPoints = atentionPoints
        self.availableTransactions = availableTransactions
