# ==============================
# DMMT TOOLKIT
# ==============================

# ------------------------------
# BST IMPLEMENTATION
# ------------------------------

class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if node is None:
            return BSTNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        if node.key == key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.key)
            self._inorder(node.right, result)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)

        elif key > node.key:
            node.right = self._delete(node.right, key)

        else:
            # Case 1: No child
            if node.left is None and node.right is None:
                return None

            # Case 2: One child
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Case 3: Two children
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current


# ------------------------------
# GRAPH IMPLEMENTATION
# ------------------------------

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v, w):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v, w))

    def print_graph(self):
        for node in self.graph:
            print(node, "->", self.graph[node])

    def bfs(self, start):
        visited = set()
        queue = [start]

        print("BFS:", end=" ")

        while queue:
            node = queue.pop(0)
            if node not in visited:
                print(node, end=" ")
                visited.add(node)
                for neighbor, _ in self.graph.get(node, []):
                    queue.append(neighbor)
        print()

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
            print("DFS:", end=" ")

        visited.add(start)
        print(start, end=" ")

        for neighbor, _ in self.graph.get(start, []):
            if neighbor not in visited:
                self.dfs(neighbor, visited)


# ------------------------------
# HASH TABLE (SEPARATE CHAINING)
# ------------------------------

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        self.table[index].append((key, value))

    def get(self, key):
        index = self.hash_function(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        index = self.hash_function(key)
        self.table[index] = [pair for pair in self.table[index] if pair[0] != key]

    def display(self):
        for i, bucket in enumerate(self.table):
            print(i, "->", bucket)


# ------------------------------
# MAIN FUNCTION (TEST CASES)
# ------------------------------

def main():
    print("\n====== BST TEST ======")
    bst = BST()

    values = [50, 30, 70, 20, 40, 60, 80]
    for v in values:
        bst.insert(v)

    print("Inorder:", bst.inorder())

    print("Search 20:", bst.search(20))
    print("Search 90:", bst.search(90))

    # Delete leaf
    bst.delete(20)
    print("After deleting 20:", bst.inorder())

    # One child case
    bst.insert(65)
    bst.delete(60)
    print("After deleting 60:", bst.inorder())

    # Two children case
    bst.delete(50)
    print("After deleting 50:", bst.inorder())

    print("\n====== GRAPH TEST ======")
    g = Graph()

    edges = [
        ('A','B',2), ('A','C',4), ('B','D',7), ('B','E',3),
        ('C','E',1), ('D','F',5), ('E','D',2),
        ('E','F',6), ('C','F',8)
    ]

    for u, v, w in edges:
        g.add_edge(u, v, w)

    g.print_graph()
    g.bfs('A')
    g.dfs('A')
    print()

    print("\n====== HASH TABLE TEST ======")
    ht = HashTable(5)

    keys = [10, 15, 20, 7, 12]
    for k in keys:
        ht.insert(k, k*10)

    ht.display()

    print("Get 10:", ht.get(10))
    print("Get 7:", ht.get(7))

    ht.delete(15)
    print("After deleting 15:")
    ht.display()


if __name__ == "__main__":
    main()