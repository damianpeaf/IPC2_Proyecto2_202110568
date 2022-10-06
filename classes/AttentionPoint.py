from classes.Client import Client
from classes.Desktop import Desktop
from core.Queue import Queue
from core.Stack import Stack


class AttentionPoint():

    def __init__(self, id, name, address):
        self.id = id
        self.name: str = name
        self.address = address
        self.activeDesktops = Stack[Desktop]()
        self.inactiveDesktops = Stack[Desktop]()
        self.clients = Queue[Client]()

        self.haveToDeactivateDesktop = False

        self.alarm = ""

        self.initSimulationProps()

    def getAsStr(self):
        return "- ID: " + self.id + "\t\n- Nombre: " + self.name + "\t\n- Dirección: " + self.address + "\n"

    def getActiveDesktopsAsStr(self):

        if self.activeDesktops.isEmpty():
            return " - "
        else:
            result = ""
            for i in range(0, self.activeDesktops.size):
                desktop = self.activeDesktops.getItem(i)

                result += desktop.getAsStr()
                result += "\n\n"

            return result

    def getInactiveDesktopsAsStr(self):

        if self.inactiveDesktops.isEmpty():
            return " - "
        else:
            result = ""
            for i in range(0, self.inactiveDesktops.size):
                desktop = self.inactiveDesktops.getItem(i)

                result += desktop.getAsStr()
                result += "\n\n"

            return result

    def initSimulationProps(self):

        self.averageWaitingTime = 0
        self.maximumWaitingTime = 0
        self.minimumWaitingTime = 0
        self.totalWaitingTime = 0

        self.averageAttentionTime = 0
        self.maximumAttentionTime = 0
        self.minimumAttentionTime = 0
        self.totalAttentionTime = 0

    def _fillDesktops(self):
        # If there are clients in queue
        if self.clients.size != 0:

            # finds the first available desktop
            for i in range(0, self.activeDesktops.size):
                desktop = self.activeDesktops.getItem(i)

                # if the desktop is available
                if desktop.canAttendClient():
                    client = self.clients.dequeue()
                    self.alarm += f"Puede pasar {client.name} a la mesa {desktop.id}\n\t"
                    if client:
                        desktop.attendClient(client)

    def elapsedOneSecond(self):

        # Deactivate desktop if it's necessary

        self._evalDeactivateDesktop()

        # Fill desktops if its posible
        self._fillDesktops()

        # Work on clients transactions

        for i in range(0, self.activeDesktops.size):
            desktop = self.activeDesktops.getItem(i)
            desktop.workOnNextClientransaction()

        # Fill desktops for ended transactions
        self._fillDesktops()
        # Update waited time for each client in queue

        for i in range(0, self.clients.size):
            client = self.clients.getItem(i)
            client.waitOneSecond()

        self.recalculateSimulationProps()

    def addClient(self, client):
        self.clients.enqueue(client)

    def recalculateSimulationProps(self):

        # * Attendance times

        totalAttentionAverageTime = 0
        for i in range(0, self.activeDesktops.size):
            desktop = self.activeDesktops.getItem(i)

            totalAttentionAverageTime += desktop.averageAttentionTime

            if i == 0:
                self.maximumAttentionTime = desktop.maximumAttentionTime
                self.minimumWaitingTime = self.minimumAttentionTime = desktop.minimumAttentionTime

            if desktop.maximumAttentionTime > self.maximumAttentionTime:
                self.maximumAttentionTime = desktop.maximumAttentionTime

            if desktop.minimumAttentionTime < self.minimumAttentionTime:
                self.minimumWaitingTime = self.minimumAttentionTime = desktop.minimumAttentionTime

        for i in range(0, self.activeDesktops.size):
            desktop = self.activeDesktops.getItem(i)

            totalAttentionAverageTime += desktop.averageAttentionTime

            if i == 0 and self.activeDesktops.size == 0:
                self.maximumAttentionTime = desktop.maximumAttentionTime
                self.minimumAttentionTime = desktop.minimumAttentionTime

            if desktop.maximumAttentionTime > self.maximumAttentionTime:
                self.maximumAttentionTime = desktop.maximumAttentionTime

            if desktop.minimumAttentionTime < self.minimumAttentionTime:
                self.minimumAttentionTime = desktop.minimumAttentionTime

        self.averageAttentionTime = totalAttentionAverageTime / (self.activeDesktops.size + self.inactiveDesktops.size)

        # * Waiting times

        # Average waiting time

        if self.clients.size != 0:

            self.maximumWaitingTime = 0
            totalWaitingAverageTime = 0
            for i in range(0, self.clients.size-1):
                client = self.clients.getItem(i)
                totalWaitingAverageTime += (float(client.getTransactionTotalTimeAsStr())+self.averageAttentionTime)
                self.maximumWaitingTime += float(client.getTransactionTotalTimeAsStr())

            self.maximumWaitingTime += self.maximumAttentionTime

            n = 1

            if self.clients.size-1 != 0:
                n = self.clients.size-1

            if totalWaitingAverageTime != 0:
                self.averageWaitingTime = totalWaitingAverageTime / n
            else:
                self.averageWaitingTime = (self.maximumWaitingTime + self.minimumWaitingTime) / 2

    def getDestopSimulationPropsAsStr(self):
        result = ""

        for i in range(0, self.activeDesktops.size):
            desktop = self.activeDesktops.getItem(i)
            result += desktop.getSimulationPropsAsStr()
            result += "\n"

        return result

    def _evalDeactivateDesktop(self):
        if self.haveToDeactivateDesktop:
            if self.activeDesktops.size > 0:

                desktopToDeactivate = self.activeDesktops.getItem(0)

                if desktopToDeactivate.canAttendClient():
                    self.activeDesktops.pop()
                    self.inactiveDesktops.push(desktopToDeactivate)

                    self.haveToDeactivateDesktop = False

    def activateDesktop(self):
        if self.inactiveDesktops.size > 0:
            desktopToActivate = self.inactiveDesktops.getItem(0)

            self.inactiveDesktops.pop()
            self.activeDesktops.push(desktopToActivate)
            return True
        return False

    def endNextClientTransaction(self, updateTime):
        client = self.clients.getItem(0)

        if client is None:
            return False

        transactionsCount = 1

        while transactionsCount > 0:
            self.elapsedOneSecond()
            updateTime()
            transactionsCount = client.transactions.size

    def getTotalAttendedClients(self):
        total = 0

        for i in range(0, self.activeDesktops.size):
            desktop = self.activeDesktops.getItem(i)
            total += desktop.clientsAttended

        for i in range(0, self.inactiveDesktops.size):
            desktop = self.inactiveDesktops.getItem(i)
            total += desktop.clientsAttended

        return total

    def isDesktopAttending(self):

        if self.activeDesktops.size <= 0:
            return False

        for i in range(0, self.activeDesktops.size):
            desktop = self.activeDesktops.getItem(i)

            if desktop is None:
                continue

            if desktop.attendentClient is not None:
                return True

        return False

    def getSimulationPropsAsStr(self):
        return f"""
        INFORMACIÓN PUNTO DE ATENCIÓN
        Escritorios activos: {str(round(self.activeDesktops.size,2))}
        Escritorios inactivos: {str(round(self.inactiveDesktops.size,2))}
        Clientes en cola: {str(round(self.clients.size,2))}
        Clientes atendidos: {str(round(self.getTotalAttendedClients(),2))}

        Tiempo promedio de espera: {str(round(self.averageWaitingTime,2))}
        Tiempo máximo de espera: {str(round(self.maximumWaitingTime,2))}
        Tiempo mínimo de espera: {str(round(self.minimumWaitingTime,2))}

        Tiempo promedio de atención: {str(round(self.averageAttentionTime,2))}
        Tiempo máximo de atención: {str(round(self.maximumAttentionTime,2))}
        Tiempo mínimo de atención: {str(round(self.minimumAttentionTime,2))}

        ALARMAS DISPARADAS: 
        {self.alarm}
        
        ESTADO ACTUAL DE LOS ESCRITORIOS:

{self.getDestopSimulationPropsAsStr()}

        """
