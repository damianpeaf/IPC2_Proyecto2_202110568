
from classes.Client import Client


class Desktop():

    def __init__(self, id, identification, attendant):
        self.id = id
        self.identification = identification
        self.attendant = attendant
        self.attendentClient = None
        self.initSimulationProps()

    def getAsStr(self):
        return "- ID: " + self.id + "\n- Identificación: " + self.identification + "\n- Encargado: " + self.attendant + "\n"

    def attendClient(self, client):
        self.attendentClient = client

    def initSimulationProps(self):
        self.averageAttentionTime = 0
        self.maximumAttentionTime = 0
        self.minimumAttentionTime = 0
        self.totalAttentionTime = 0

    def canAttendClient(self):
        return self.attendentClient is None

    def workOnNextClientransaction(self):

        nextTransaction = self.attendentClient.transactions.getItem(0)
        if nextTransaction:
            nextTransaction.workOneSecond()
            self.recalculateSimulationProps()
            return True
        else:
            # * No more transactions
            return False

    def finishCurrentClientAttention(self):
        self.attendentClient = None

    def recalculateSimulationProps(self):

        numberOfTransactions = self.attendentClient.transactions.size

        if numberOfTransactions <= 0:
            return

        self.averageAttentionTime = 0
        for i in range(0, numberOfTransactions):
            actualTransaction = self.attendentClient.transactions.getItem(i)
            nextTransaction = self.attendentClient.transactions.getItem(i+1)

            # minimum and maximum
            if i < numberOfTransactions-2:
                if nextTransaction.pendingTime < actualTransaction.pendingTime:
                    self.minimumAttentionTime = nextTransaction.pendingTime

                if actualTransaction.pendingTime < nextTransaction.pendingTime:
                    self.maximumAttentionTime = nextTransaction.pendingTime

            self.totalAttentionTime += actualTransaction.pendingTime

        if numberOfTransactions != 0:
            self.averageAttentionTime = self.totalAttentionTime/numberOfTransactions
        else:
            self.averageAttentionTime = 0
