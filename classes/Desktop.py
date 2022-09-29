
from classes.Client import Client
from core.SimpleList import SimpleList


class Desktop():

    def __init__(self, id, identification, attendant):
        self.id = id
        self.identification = identification
        self.attendant = attendant
        self.attendentClient = None
        self.clientsAttended = 0
        self.attentionsTimes = SimpleList[float]()
        self.initSimulationProps()

    def getAsStr(self):
        return "- ID: " + self.id + "\n- Identificación: " + self.identification + "\n- Encargado: " + self.attendant + "\n"

    def attendClient(self, client: Client):
        self.attentionsTimes.addAtEnd(float(client.getTransactionTotalTimeAsStr()))
        self.attendentClient = client

    def initSimulationProps(self):
        self.averageAttentionTime = 0
        self.maximumAttentionTime = 0
        self.minimumAttentionTime = 0
        self.totalAttentionTime = 0

    def canAttendClient(self):
        return self.attendentClient is None

    def workOnNextClientransaction(self):

        if self.attendentClient is None:
            return

        nextTransaction = self.attendentClient.transactions.getItem(0)
        if nextTransaction:
            nextTransaction.workOneSecond()
            self.recalculateSimulationProps()

            if nextTransaction.pendingTime <= 0:
                self.attendentClient.transactions.deleteAtStart()

            return True
        else:
            self.finishCurrentClientAttention()
            # * No more transactions
            return False

    def finishCurrentClientAttention(self):
        self.clientsAttended += 1
        self.attendentClient = None

    def recalculateSimulationProps(self):

        if self.attentionsTimes.size == 0:
            return

        posibleMax = posibleMin = self.attentionsTimes.getItem(0)

        for i in range(0, self.attentionsTimes.size):
            time = self.attentionsTimes.getItem(i)
            if time > posibleMax:
                posibleMax = time
            if time < posibleMin:
                posibleMin = time

        self.maximumAttentionTime = posibleMax
        self.minimumAttentionTime = posibleMin

        totalTimes = 0

        for i in range(0, self.attentionsTimes.size):
            totalTimes += self.attentionsTimes.getItem(i)
        self.averageAttentionTime = totalTimes/self.attentionsTimes.size

    def getSimulationPropsAsStr(self):
        return f"""
        
        Escritorio: {self.id} -  Servidor: {self.attendant} -  Clientes atendidos: {str(self.clientsAttended)}
        - Tiempo promedio de atención: {str(self.averageAttentionTime)}
        - Tiempo máximo de atención: {str(self.maximumAttentionTime)}
        - Tiempo mínimo de atención: {str(self.minimumAttentionTime)}
        - Ateniendo a: {self.attendentClient.name}
        - Trabajando en: 
        {self.attendentClient.getTransactionsAsStr()}
        """ if self.attendentClient is not None else f"""
        Escritorio Libre: {self.id} -  Servidor: {self.attendant} -  Clientes atendidos: {str(self.clientsAttended)}
        """
