

from typing import Generic, TypeVar
from core.Node import Node

T = TypeVar('T')


class SimpleList(Generic[T]):

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def isEmpty(self):
        return self.size == 0

    def addAtStart(self, data):
        newNode = Node[T](data)

        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            newNode.next = self.tail
            self.tail = newNode
        self.size += 1

    def addAtEnd(self, data):

        newNode = Node[T](data)

        if self.isEmpty():
            self.head = newNode
            self.tail = newNode
        else:
            self.head.next = newNode
            self.head = newNode
        self.size += 1

    def deleteAtStart(self):
        if self.isEmpty():
            return None
        elif self.tail == self.head:
            self.tail = None
            self.head = None
        else:
            self.tail = self.tail.next
            self.size -= 1

    def deleteAtEnd(self):
        if self.isEmpty():
            return None
        elif self.tail == self.head:
            self.tail = None
            self.head = None
        else:
            current = self.tail
            while current.next != self.head:
                current = current.next
            current.next = None
            self.head = current
            self.size -= 1

    def getItem(self, index):
        if self.isEmpty():
            return None

        counter = 0

        current = self.tail

        while current is not None:
            if counter == index:
                return current.data
            current = current.next
            counter += 1

        return None
