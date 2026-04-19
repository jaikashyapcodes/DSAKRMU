"""
algorithms.py - BFS and DFS for relationship discovery
"""

from collections import deque


def bfs_shortest_path(adj, src, dst):
    if src not in adj:
        print(f"  [ERROR] '{src}' not in graph.")
        return []
    if dst not in adj:
        print(f"  [ERROR] '{dst}' not in graph.")
        return []
    if src == dst:
        return [src]

    seen = {src}
    q = deque([[src]])

    while q:
        path = q.popleft()
        node = path[-1]
        for nb in adj.get(node, []):
            if nb == dst:
                return path + [nb]
            if nb not in seen:
                seen.add(nb)
                q.append(path + [nb])
    return []


def dfs_friends_of_friends(adj, start, max_depth):
    if start not in adj:
        print(f"  [ERROR] '{start}' not in graph.")
        return {}

    found = {}
    visited = {start}

    def _dfs(node, depth):
        if depth > max_depth:
            return
        for nb in adj.get(node, []):
            if nb not in visited:
                visited.add(nb)
                found[nb] = depth
                _dfs(nb, depth + 1)

    _dfs(start, 1)
    return found


def print_bfs_result(src, dst, path):
    print(f"\n  BFS  [{src}] → [{dst}]")
    if not path:
        print(f"  No path found.")
    else:
        print(f"  Hops : {len(path) - 1}")
        print(f"  Path : {' ──► '.join(path)}")


def print_dfs_result(start, depth, reachable):
    print(f"\n  DFS  (start='{start}', depth={depth})")
    if not reachable:
        print(f"  Nothing reachable within depth {depth}.")
        return
    by_depth = {}
    for uid, d in sorted(reachable.items(), key=lambda x: (x[1], x[0])):
        by_depth.setdefault(d, []).append(uid)
    for d in sorted(by_depth):
        print(f"  Level {d}: {', '.join(by_depth[d])}")
    print(f"  Total: {len(reachable)} users")
