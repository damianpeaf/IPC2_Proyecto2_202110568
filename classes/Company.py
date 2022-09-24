
from multiprocessing.connection import Client
from classes.AttentionPoint import AttentionPoint
from classes.TransactionType import TransactionType
from core.Queue import Queue
from core.SimpleList import SimpleList


class Company():

    def __init__(self, id, name: str, abbreviaton: str):

        self.id = id
        self.name = name
        self.abbreviaton = abbreviaton
        self.attentionPoints = SimpleList[AttentionPoint]()
        self.availableTransactions = SimpleList[TransactionType]()
        self.clients = Queue[Client]()
