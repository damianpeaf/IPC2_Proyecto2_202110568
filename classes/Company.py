
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

    def getAtentionPointsAsStr(self):

        if self.attentionPoints.isEmpty():
            return " - "
        else:
            result = ""
            for i in range(0, self.attentionPoints.size):
                attentionpoint = self.attentionPoints.getItem(i)

                result += "[blue] PUNTO DE ATENCION [/blue] \n"

                result += attentionpoint.getAsStr()

                result += "\n [blue] ESCRITORIOS [/blue] \n\n"

                result += " [green] ACTIVOS [/green] \n"

                result += attentionpoint.getActiveDesktopsAsStr()

                result += "\n [red] INACTIVOS [/red] \n"

                result += attentionpoint.getInactiveDesktopsAsStr()

                result += "\n\n"

            return result

    def getAvailableTransactions(self):

        if self.availableTransactions.isEmpty():
            return " - "
        else:
            result = ""
            for i in range(0, self.availableTransactions.size):
                transactionType = self.availableTransactions.getItem(i)

                result += transactionType.getAsStr() + "\n"

            return result
