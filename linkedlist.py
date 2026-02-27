#!/usr/bin/env python3


class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, val):
        new_node = Node(val)
        if self.head is None:
            self.head = new_node
            return

        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = new_node

    def prepend(self, val):
        self.head = Node(val, self.head)

    def delete(self, val):
        if self.head is None:
            return

        if self.head.value == val:
            self.head = self.head.next
            return

        prev = self.head
        curr = self.head.next
        while curr is not None:
            if curr.value == val:
                prev.next = curr.next
                return
            prev = curr
            curr = curr.next

    def to_list(self):
        out = []
        curr = self.head
        while curr is not None:
            out.append(curr.value)
            curr = curr.next
        return out
