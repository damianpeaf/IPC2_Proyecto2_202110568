from classes.Desktop import Desktop
from core.Stack import Stack


class AttentionPoint():

    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address
        self.activeDesktops = Stack[Desktop]()
        self.inactiveDesktops = Stack[Desktop]()
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
        self.activeDesktopsCount = self.activeDesktops.size
        self.inactiveDesktopsCount = self.inactiveDesktops.size

        self.clientsInQueue = 0

        self.averageWaitingTime = 0
        self.maximumWaitingTime = 0
        self.minimumWaitingTime = 0

        self.averageAttentionTime = 0
        self.maximumAttentionTime = 0
        self.minimumAttentionTime = 0
        self.recalculateSimulationProps()

    def recalculateSimulationProps(self):
        pass
