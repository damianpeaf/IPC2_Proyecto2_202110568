

from typing import Generic, TypeVar
from core.SimpleList import SimpleList

T = TypeVar('T')


class Stack(Generic[T]):

    def __init__(self):
        self._list = SimpleList[T]()
        self.size = 0

    def isEmpty(self):
        return self._list.isEmpty()

    def push(self, data: T):
        self._list.addAtStart(data)
        self.size += 1

    def popNode(self, node: T):

        for i in range(0, self._list.size):
            evalNode = self._list.getItem(i)
            if evalNode == node:
                self._list.deleteAtIndex(i)
                self.size -= 1
                return evalNode

        return None

    def getItem(self, index: int):
        return self._list.getItem(index)

    def pop(self):
        aux = self._list.tail.data
        self._list.deleteAtStart()
        self.size -= 1

        return aux
