

from typing import Generic, TypeVar

from core.SimpleList import SimpleList

T = TypeVar('T')


class Queue(Generic[T]):

    def __init__(self):
        self._simpleList = SimpleList[T]()
        self.size = 0

    def isEmpty(self):
        return self._simpleList.isEmpty()

    def enqueue(self, data: T):

        self._simpleList.addAtEnd(data)
        self.size += 1

    def dequeue(self):
        aux = self._simpleList.tail.data
        self._simpleList.deleteAtStart()
        self.size -= 1
        return aux
