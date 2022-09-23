
from typing import Generic, TypeVar


T = TypeVar('T')


class Node(Generic[T]):

    def __init__(self, data):
        self.data: T = data
        self.next = None
