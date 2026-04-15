"""
network_graph.py - adjacency list graph for the friend/follower network
"""


class SocialGraph:
    def __init__(self, directed=False):
        self.adj = {}
        self.directed = directed

    def _init_node(self, uid):
        if uid not in self.adj:
            self.adj[uid] = set()

    def add_node(self, uid):
        self._init_node(uid)

    def remove_node(self, uid):
        if uid not in self.adj:
            return
        del self.adj[uid]
        for nbrs in self.adj.values():
            nbrs.discard(uid)

    def add_friendship(self, a, b, pm=None):
        if pm:
            if not pm.user_exists(a):
                print(f"  [ERROR] User '{a}' does not exist.")
                return False
            if not pm.user_exists(b):
                print(f"  [ERROR] User '{b}' does not exist.")
                return False
        self._init_node(a)
        self._init_node(b)
        if b in self.adj[a]:
            print(f"  [WARN] {a} ↔ {b} already connected.")
            return False
        self.adj[a].add(b)
        if not self.directed:
            self.adj[b].add(a)
        return True

    def remove_friendship(self, a, b):
        if a not in self.adj or b not in self.adj[a]:
            print(f"  [ERROR] No connection between '{a}' and '{b}'.")
            return False
        self.adj[a].discard(b)
        if not self.directed:
            self.adj[b].discard(a)
        return True

    def get_friends(self, uid):
        if uid not in self.adj:
            print(f"  [ERROR] '{uid}' not in graph.")
            return []
        return sorted(self.adj[uid])

    def are_connected(self, a, b):
        return a in self.adj and b in self.adj[a]

    def all_nodes(self):
        return list(self.adj.keys())

    def get_adjacency(self):
        return self.adj

    def display_connections(self, uid):
        friends = self.get_friends(uid)
        label = "Followers" if self.directed else "Friends"
        if not friends:
            print(f"  {uid} has no {label.lower()} yet.")
        else:
            print(f"  {label} of '{uid}': {' → '.join(friends)}")

    def display_full_graph(self):
        print("\n  === Adjacency List ===")
        for node in sorted(self.adj):
            print(f"  {node:12s} : {sorted(self.adj[node])}")
