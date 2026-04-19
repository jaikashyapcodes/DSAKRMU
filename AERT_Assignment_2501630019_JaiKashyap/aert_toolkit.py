# aert_toolkit.py
# Algorithmic Efficiency & Recursion Toolkit - Unit 1 Assignment
# ETCCDS202 - Data Structures


# ── Stack ADT ────────────────────────────────────────────────────────

class StackADT:
    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.is_empty():
            print("  [error] stack underflow")
            return None
        return self.data.pop()

    def peek(self):
        if self.is_empty():
            print("  [error] stack is empty")
            return None
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)


# ── Factorial ────────────────────────────────────────────────────────

def factorial(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


# ── Fibonacci ────────────────────────────────────────────────────────

call_count = 0

def fib_naive(n):
    global call_count
    call_count += 1
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


memo_count = 0

def fib_memo(n, memo=None):
    global memo_count
    memo_count += 1
    if memo is None:
        memo = {}
    if n <= 1:
        return n
    if n in memo:
        return memo[n]
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]


# ── Tower of Hanoi ───────────────────────────────────────────────────

hanoi_moves = StackADT()

def hanoi(n, src, aux, dst):
    if n == 1:
        move = f"Move disk 1 from {src} to {dst}"
        print(" ", move)
        hanoi_moves.push(move)
        return
    hanoi(n - 1, src, dst, aux)
    move = f"Move disk {n} from {src} to {dst}"
    print(" ", move)
    hanoi_moves.push(move)
    hanoi(n - 1, aux, src, dst)


# ── Binary Search ────────────────────────────────────────────────────

mid_stack = StackADT()

def binary_search(arr, key, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    mid_stack.push(mid)
    if arr[mid] == key:
        return mid
    elif arr[mid] < key:
        return binary_search(arr, key, mid + 1, high)
    else:
        return binary_search(arr, key, low, mid - 1)


# ── Main ─────────────────────────────────────────────────────────────

def section(title):
    print("\n" + "=" * 52)
    print(" " + title)
    print("=" * 52)


def main():

    # Part A: Stack ADT demo
    section("Part A: Stack ADT")
    st = StackADT()
    for v in [10, 20, 30]:
        st.push(v)
    print(f"  push 10, 20, 30 | peek = {st.peek()} | size = {st.size()}")
    print(f"  pop = {st.pop()} | size = {st.size()}")
    print(f"  is_empty = {st.is_empty()}")
    st.pop(); st.pop()
    print(f"  after popping all | is_empty = {st.is_empty()}")
    st.pop()  # underflow

    # Part B: Factorial
    section("Part B: Factorial")
    for n in [0, 1, 5, 10]:
        print(f"  factorial({n}) = {factorial(n)}")
    try:
        factorial(-3)
    except ValueError as e:
        print(f"  factorial(-3) -> ValueError: {e}")

    # Part B: Fibonacci
    section("Part B: Fibonacci")
    print(f"  {'n':<6} {'fib':<10} {'naive calls':<16} {'memo calls'}")
    print("  " + "-" * 46)
    for n in [5, 10, 20, 30]:
        global call_count, memo_count
        call_count = 0
        result_naive = fib_naive(n)
        nc = call_count

        memo_count = 0
        result_memo = fib_memo(n)
        mc = memo_count

        print(f"  {n:<6} {result_naive:<10} {nc:<16} {mc}")

    # Part C: Tower of Hanoi
    section("Part C: Tower of Hanoi (N=3)")
    hanoi(3, "A", "B", "C")
    print(f"\n  Total moves: {hanoi_moves.size()} (expected: {2**3 - 1})")

    # Part D: Binary Search
    section("Part D: Recursive Binary Search")
    arr = [1, 3, 5, 7, 9, 11, 13]
    print(f"  Array: {arr}")
    for key in [7, 1, 13, 2]:
        mid_stack = StackADT()  # reset for each search
        idx = binary_search(arr, key, 0, len(arr) - 1)
        print(f"  search({key}) -> index {idx}")

    print("\n  Edge case: empty array")
    result = binary_search([], 5, 0, -1)
    print(f"  search(5) in [] -> index {result}")


if __name__ == "__main__":
    main()
