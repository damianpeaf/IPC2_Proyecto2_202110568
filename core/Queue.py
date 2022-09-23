

from typing import Generic, TypeVar

from core.SimpleList import SimpleList

T = TypeVar('T')


class Queue(Generic[T]):

    def __init__(self):
        self._simpleList = SimpleList[T]()
        self.size = self._simpleList.size

    def isEmpty(self):
        return self._simpleList.isEmpty()

    def enqueue(self, data):
        self._simpleList.addAtEnd(data)

    def dequeue(self):
        aux = self._simpleList.tail.data
        self._simpleList.deleteAtStart()
        return aux
