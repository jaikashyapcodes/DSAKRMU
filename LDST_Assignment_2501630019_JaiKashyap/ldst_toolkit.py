# ldst_toolkit.py
# Linear Data Structures Toolkit - Unit 2 Assignment
# ETCCDS202 - Data Structures


# ── Dynamic Array ────────────────────────────────────────────────────

class DynamicArray:
    def __init__(self, capacity=2):
        self.capacity = capacity
        self.size = 0
        self.data = [None] * self.capacity

    def _resize(self):
        new_capacity = self.capacity * 2
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity
        print(f"  [resize] capacity doubled to {self.capacity}")

    def append(self, x):
        if self.size == self.capacity:
            self._resize()
        self.data[self.size] = x
        self.size += 1

    def pop(self):
        if self.size == 0:
            print("  [error] array is empty")
            return None
        val = self.data[self.size - 1]
        self.data[self.size - 1] = None
        self.size -= 1
        return val

    def __str__(self):
        elements = [str(self.data[i]) for i in range(self.size)]
        return "[" + ", ".join(elements) + f"]  (size={self.size}, capacity={self.capacity})"


# ── Singly Linked List ───────────────────────────────────────────────

class SNode:
    def __init__(self, val):
        self.val = val
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, x):
        node = SNode(x)
        node.next = self.head
        self.head = node

    def insert_at_end(self, x):
        node = SNode(x)
        if self.head is None:
            self.head = node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = node

    def delete_by_value(self, x):
        if self.head is None:
            print(f"  [error] list is empty, cannot delete {x}")
            return
        if self.head.val == x:
            self.head = self.head.next
            return
        cur = self.head
        while cur.next and cur.next.val != x:
            cur = cur.next
        if cur.next is None:
            print(f"  [error] value {x} not found")
        else:
            cur.next = cur.next.next

    def traverse(self):
        elems = []
        cur = self.head
        while cur:
            elems.append(str(cur.val))
            cur = cur.next
        print("  SLL:", " -> ".join(elems) if elems else "(empty)")


# ── Doubly Linked List ───────────────────────────────────────────────

class DNode:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_end(self, x):
        node = DNode(x)
        if self.head is None:
            self.head = self.tail = node
            return
        node.prev = self.tail
        self.tail.next = node
        self.tail = node

    def insert_after_node(self, target, x):
        cur = self.head
        while cur and cur.val != target:
            cur = cur.next
        if cur is None:
            print(f"  [error] target {target} not found")
            return
        node = DNode(x)
        node.next = cur.next
        node.prev = cur
        if cur.next:
            cur.next.prev = node
        else:
            self.tail = node
        cur.next = node

    def delete_at_position(self, pos):
        # 0-based
        cur = self.head
        idx = 0
        while cur and idx < pos:
            cur = cur.next
            idx += 1
        if cur is None:
            print(f"  [error] position {pos} out of range")
            return
        if cur.prev:
            cur.prev.next = cur.next
        else:
            self.head = cur.next
        if cur.next:
            cur.next.prev = cur.prev
        else:
            self.tail = cur.prev

    def traverse(self):
        elems = []
        cur = self.head
        while cur:
            elems.append(str(cur.val))
            cur = cur.next
        print("  DLL:", " <-> ".join(elems) if elems else "(empty)")


# ── Stack (using SinglyLinkedList) ───────────────────────────────────

class Stack:
    def __init__(self):
        self.sll = SinglyLinkedList()
        self.size = 0

    def push(self, x):
        self.sll.insert_at_beginning(x)
        self.size += 1

    def pop(self):
        if self.sll.head is None:
            print("  [error] stack underflow")
            return None
        val = self.sll.head.val
        self.sll.head = self.sll.head.next
        self.size -= 1
        return val

    def peek(self):
        if self.sll.head is None:
            print("  [error] stack is empty")
            return None
        return self.sll.head.val

    def is_empty(self):
        return self.sll.head is None


# ── Queue (using SinglyLinkedList) ───────────────────────────────────

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, x):
        node = SNode(x)
        if self.tail:
            self.tail.next = node
        self.tail = node
        if self.head is None:
            self.head = node
        self.size += 1

    def dequeue(self):
        if self.head is None:
            print("  [error] queue underflow")
            return None
        val = self.head.val
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return val

    def front(self):
        if self.head is None:
            print("  [error] queue is empty")
            return None
        return self.head.val


# ── Balanced Parentheses Checker ─────────────────────────────────────

def is_balanced(expr):
    stack = Stack()
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in expr:
        if ch in '([{':
            stack.push(ch)
        elif ch in ')]}':
            if stack.is_empty() or stack.peek() != pairs[ch]:
                return False
            stack.pop()
    return stack.is_empty()


# ── Main / Test Runner ───────────────────────────────────────────────

def section(title):
    print("\n" + "=" * 55)
    print(" " + title)
    print("=" * 55)


def main():
    # ── Task 1: Dynamic Array ──────────────────────────────────
    section("Task 1: Dynamic Array")

    arr = DynamicArray(capacity=2)
    print("Appending 12 elements (initial capacity = 2):")
    for i in range(1, 13):
        arr.append(i * 10)
    print(" ", arr)

    print("\nPopping 3 elements:")
    for _ in range(3):
        val = arr.pop()
        print(f"  popped {val} ->", arr)

    # ── Task 2A: Singly Linked List ────────────────────────────
    section("Task 2A: Singly Linked List")

    sll = SinglyLinkedList()
    print("Insert at beginning: 30, 20, 10")
    sll.insert_at_beginning(30)
    sll.insert_at_beginning(20)
    sll.insert_at_beginning(10)
    sll.traverse()

    print("Insert at end: 40, 50, 60")
    sll.insert_at_end(40)
    sll.insert_at_end(50)
    sll.insert_at_end(60)
    sll.traverse()

    print("Delete by value: 20")
    sll.delete_by_value(20)
    sll.traverse()

    print("Delete by value: 99 (not in list)")
    sll.delete_by_value(99)

    # ── Task 2B: Doubly Linked List ────────────────────────────
    section("Task 2B: Doubly Linked List")

    dll = DoublyLinkedList()
    for v in [10, 20, 30, 40, 50]:
        dll.insert_at_end(v)
    print("Initial DLL:")
    dll.traverse()

    print("Insert 25 after node with value 20:")
    dll.insert_after_node(20, 25)
    dll.traverse()

    print("Delete at position 1 (0-based):")
    dll.delete_at_position(1)
    dll.traverse()

    print("Delete at last position (pos=4):")
    dll.delete_at_position(4)
    dll.traverse()

    # ── Task 3A: Stack ─────────────────────────────────────────
    section("Task 3A: Stack (using SinglyLinkedList)")

    st = Stack()
    print("Pushing: 5, 10, 15, 20")
    for v in [5, 10, 15, 20]:
        st.push(v)
    print(f"  peek = {st.peek()}")
    print(f"  pop  = {st.pop()}")
    print(f"  pop  = {st.pop()}")
    print(f"  peek = {st.peek()}")
    print(f"  size = {st.size}")
    print("Popping remaining:")
    while not st.is_empty():
        print(f"  pop = {st.pop()}")
    print("Pop on empty stack:")
    st.pop()

    # ── Task 3B: Queue ─────────────────────────────────────────
    section("Task 3B: Queue (using SinglyLinkedList)")

    q = Queue()
    print("Enqueue: A, B, C, D")
    for v in ["A", "B", "C", "D"]:
        q.enqueue(v)
    print(f"  front = {q.front()}")
    print(f"  dequeue = {q.dequeue()}")
    print(f"  dequeue = {q.dequeue()}")
    print(f"  front = {q.front()}")
    print(f"  size = {q.size}")
    print("Dequeue remaining:")
    while q.head:
        print(f"  dequeue = {q.dequeue()}")
    print("Dequeue on empty queue:")
    q.dequeue()

    # ── Task 4: Balanced Parentheses Checker ───────────────────
    section("Task 4: Balanced Parentheses Checker")

    tests = [
        ("([])",   True),
        ("([)]",   False),
        ("(((", False),
        ("",       True),
        ("{[()]}",  True),
        ("((()))",  True),
        ("[{]",     False),
    ]
    print(f"  {'Expression':<15} {'Expected':<12} {'Got':<12} {'Pass?'}")
    print("  " + "-" * 48)
    for expr, expected in tests:
        result = is_balanced(expr)
        status = "PASS" if result == expected else "FAIL"
        label = repr(expr) if expr else '""'
        print(f"  {label:<15} {str(expected):<12} {str(result):<12} {status}")


if __name__ == "__main__":
    main()
