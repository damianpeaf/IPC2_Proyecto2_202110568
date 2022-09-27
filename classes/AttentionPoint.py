from classes.Client import Client
from classes.Desktop import Desktop
from core.Queue import Queue
from core.Stack import Stack


class AttentionPoint():

    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address
        self.activeDesktops = Stack[Desktop]()
        self.inactiveDesktops = Stack[Desktop]()
        self.clients = Queue[Client]()
        self.initSimulationProps()

    def getAsStr(self):
        return "- ID: " + self.id + "\n- Nombre: " + self.name + "\n- Dirección: " + self.address + "\n"

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

    def elapsedOneSecond(self):

        # Fill desktops if its posible

        # If there are clients in queue
        if self.clients.size != 0:

            # finds the first available desktop
            for i in range(0, self.activeDesktops.size):
                desktop = self.activeDesktops.getItem(i)

                # if the desktop is available
                if desktop.canAttendClient():
                    desktop.attendClient(self.clients.dequeue())

        # Work on clients transactions

        for i in range(0, self.activeDesktops.size):
            desktop = self.activeDesktops.getItem(i)
            desktop.workOnNextClientransaction()

        # Update waited time for each client in queue

        for i in range(0, self.clients.size):
            client = self.clients.getItem(i)
            client.waitOneSecond()

        self.recalculateSimulationProps()

    def recalculateSimulationProps(self):

        # average, minimun and maximum waiting time
        self.totalWaitingTime = 0
        for i in range(0, self.clients.size):
            actualClient = self.clients.getItem(i)
            nextClient = self.clients.getItem(i+1)

            if i < self.clients.size - 2:
                if nextClient.waitedTime < actualClient.waitedTime:
                    self.minimumWaitingTime = nextClient.waitedTime
                elif nextClient.waitedTime > actualClient.waitedTime:
                    self.maximumWaitingTime = nextClient.waitedTime

            self.totalWaitingTime += actualClient.waitedTime

        if self.clients.size != 0:
            self.averageWaitingTime = self.totalWaitingTime / self.clients.size
        else:
            self.averageWaitingTime = 0

        # average, minimun and maximum attedance time
        self.totalAttentionTime = 0
        for i in range(0, self.activeDesktops.size):
            actualDesktop = self.activeDesktops.getItem(i)
            nextDeskop = self.activeDesktops.getItem(i+1)

            self.totalAttentionTime += actualDesktop.totalAttentionTime

            if i < self.activeDesktops.size - 2:

                if nextDeskop.totalAttentionTime < actualDesktop.totalAttentionTime:
                    self.minimumAttentionTime = nextDeskop.totalAttentionTime
                if actualDesktop.totalAttentionTime < nextDeskop.totalAttentionTime:
                    self.maximumAttentionTime = nextDeskop.totalAttentionTime

        if self.activeDesktops.size != 0:
            self.averageAttentionTime = self.totalAttentionTime / self.activeDesktops.size
        else:
            self.averageAttentionTime = 0

    def getSimulationPropsAsStr(self):
        return f"""
        Escritorios activos: {str(self.activeDesktops.size)}
        Escritorios inactivos: {str(self.inactiveDesktops.size)}
        Clientes en cola: {str(self.clients.size)}

        Tiempo promedio de espera: {str(self.averageWaitingTime)}
        Tiempo máximo de espera: {str(self.maximumWaitingTime)}
        Tiempo mínimo de espera: {str(self.minimumWaitingTime)}

        Tiempo promedio de atención: {str(self.averageAttentionTime)}
        Tiempo máximo de atención: {str(self.maximumAttentionTime)}
        Tiempo mínimo de atención: {str(self.minimumAttentionTime)}
        
        """
