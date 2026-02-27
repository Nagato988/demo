#!/usr/bin/env python3

from collections import defaultdict, deque


class Graph:
    def __init__(self):
        self.adj = defaultdict(set)

    def add_edge(self, u, v):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def bfs(self, start) -> list:
        if start not in self.adj:
            return [start]

        visited = {start}
        order = []
        queue = deque([start])

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in sorted(self.adj[node]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return order

    def dfs(self, start) -> list:
        if start not in self.adj:
            return [start]

        visited = set()
        order = []

        def walk(node):
            visited.add(node)
            order.append(node)
            for neighbor in sorted(self.adj[node]):
                if neighbor not in visited:
                    walk(neighbor)

        walk(start)
        return order
