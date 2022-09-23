
from typing import List

from classes.Desktop import Desktop


class AttentionPoint():

    def __init__(self, id, name, address, desktops: List[Desktop]):
        self.id = id
        self.name = name
        self.address = address
        self.desktops = desktops
