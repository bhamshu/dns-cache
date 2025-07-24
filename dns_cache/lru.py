from __future__ import annotations

from typing import Optional


class Node:
    __slots__ = ("val", "prev", "next")

    def __init__(self, val: str):
        self.val: str = val
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class DLL:
    """Head = LRU, Tail = MRU."""

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def append(self, node: Node) -> None:
        node.prev = self.tail
        node.next = None
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self._size += 1

    def remove_node(self, node: Node) -> None:
        prev = node.prev
        nxt = node.next

        if prev:
            prev.next = nxt
        else:
            self.head = nxt

        if nxt:
            nxt.prev = prev
        else:
            self.tail = prev

        node.prev = node.next = None
        self._size -= 1

    def move_to_tail(self, node: Node) -> None:
        if node is self.tail:
            return
        self.remove_node(node)
        self.append(node)

    def pop_head(self) -> Optional[Node]:
        if not self.head:
            return None
        node = self.head
        self.remove_node(node)
        return node
