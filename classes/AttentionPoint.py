from classes.Desktop import Desktop
from core.Stack import Stack


class AttentionPoint():

    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address
        self.activeDesktops = Stack[Desktop]()
        self.inactiveDesktops = Stack[Desktop]()
