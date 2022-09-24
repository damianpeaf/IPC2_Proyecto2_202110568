from classes.Desktop import Desktop
from core.Stack import Stack


class AttentionPoint():

    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address
        self.activeDesktops = Stack[Desktop]()
        self.inactiveDesktops = Stack[Desktop]()

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
