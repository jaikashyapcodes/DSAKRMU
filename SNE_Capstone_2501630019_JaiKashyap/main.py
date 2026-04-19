"""
main.py - Social Network Explorer entry point
"""

from profiles import ProfileManager
from network_graph import SocialGraph
from algorithms import bfs_shortest_path, dfs_friends_of_friends, print_bfs_result, print_dfs_result
from sorting import get_top_suggestions, compare_sorts_demo

pm = ProfileManager()
graph = SocialGraph(directed=False)


def load_demo():
    print("\n" + "="*58)
    print("  DEMO MODE")
    print("="*58)

    people = [
        ("u1", "Alice",   22, ["sports", "tech", "music"],    "Delhi",      "Engineer"),
        ("u2", "Bob",     25, ["tech", "gaming", "travel"],   "Mumbai",     "Developer"),
        ("u3", "Carol",   21, ["music", "art", "travel"],     "Pune",       "Designer"),
        ("u4", "David",   28, ["sports", "fitness", "tech"],  "Bengaluru",  "Analyst"),
        ("u5", "Eve",     23, ["gaming", "music", "coding"],  "Chennai",    "Student"),
        ("u6", "Frank",   30, ["travel", "food", "fitness"],  "Hyderabad",  "Manager"),
        ("u7", "Grace",   24, ["art", "tech", "design"],      "Kolkata",    "Artist"),
        ("u8", "Hemanth", 27, ["coding", "sports", "music"],  "Jaipur",     "Researcher"),
    ]

    print("\n  [1] Adding users...")
    for uid, name, age, interests, city, job in people:
        ok = pm.add_user(uid, name, age, interests, city, job)
        graph.add_node(uid)
        print(f"  {'✓' if ok else '✗'}  {uid} ({name})")

    print("\n  [2] Updating profiles...")
    pm.update_user_profile("u1", bio="Loves hiking and open-source.")
    pm.update_user_profile("u3", age=22, profession="Senior Designer")
    print("  ✓ u1 bio, u3 age+profession")

    print("\n  [3] Sample profiles:")
    for uid in ("u1", "u3", "u5"):
        pm.display_profile(uid)

    connections = [
        ("u1","u2"), ("u1","u3"), ("u2","u4"),
        ("u3","u5"), ("u4","u5"), ("u4","u6"),
        ("u5","u7"), ("u6","u7"), ("u7","u8"), ("u2","u8"),
    ]
    print("\n  [4] Adding friendships...")
    for a, b in connections:
        ok = graph.add_friendship(a, b, pm)
        print(f"  {'✓' if ok else '✗'}  {a} ↔ {b}")

    print("\n  [5] Removing u4 ↔ u6...")
    graph.remove_friendship("u4", "u6")
    print("  ✓ done")

    print("\n  [6] Friend lists:")
    graph.display_connections("u1")
    graph.display_connections("u5")

    adj = graph.get_adjacency()

    print("\n  [7] BFS queries:")
    print_bfs_result("u1", "u7", bfs_shortest_path(adj, "u1", "u7"))
    print_bfs_result("u1", "u8", bfs_shortest_path(adj, "u1", "u8"))
    pm.add_user("u9", "Isolated", 19, ["yoga"], "Agra", "Freelancer")
    graph.add_node("u9")
    print_bfs_result("u1", "u9", bfs_shortest_path(adj, "u1", "u9"))

    print("\n  [8] DFS queries:")
    print_dfs_result("u1", 2, dfs_friends_of_friends(adj, "u1", 2))
    print_dfs_result("u1", 3, dfs_friends_of_friends(adj, "u1", 3))

    print("\n  [9] Top-5 suggestions for u1:")
    sugs = get_top_suggestions("u1", pm, adj, top_n=5, algo="merge")
    if sugs:
        print(f"  {'#':<4} {'ID':<8} {'Name':<12} Score")
        for i, (score, cid) in enumerate(sugs, 1):
            nm = pm.users[cid]["name"]
            print(f"  {i:<4} {cid:<8} {nm:<12} {score}")
    else:
        print("  No suggestions.")

    print("\n  [10] Sort comparison:")
    from sorting import compute_scores, build_interest_index
    idx = build_interest_index(pm)
    raw = compute_scores("u2", pm, adj, idx)
    compare_sorts_demo(raw)

    print("\n" + "="*58 + "\n")


def _inp(msg):
    return input(msg).strip()


def show_menu():
    print("""
  ╔══════════════════════════════════════════════╗
  ║       Social Network Explorer (SNE)          ║
  ╠══════════════════════════════════════════════╣
  ║  1. Add user          6. Show connections    ║
  ║  2. View profile      7. Shortest path (BFS) ║
  ║  3. Update profile    8. Friends-of-friends  ║
  ║  4. Add friendship    9. Friend suggestions  ║
  ║  5. Remove friend    10. All profiles        ║
  ║                      11. Full graph  0. Exit ║
  ╚══════════════════════════════════════════════╝""")


def do_add_user():
    uid  = _inp("  ID       : ")
    name = _inp("  Name     : ")
    age  = _inp("  Age      : ")
    ints = [x.strip() for x in _inp("  Interests: ").split(",")]
    city = _inp("  City     : ")
    job  = _inp("  Job      : ")
    bio  = _inp("  Bio      : ")
    try:
        age = int(age)
    except ValueError:
        print("  [ERROR] Age must be a number."); return
    if pm.add_user(uid, name, age, ints, city, job, bio):
        graph.add_node(uid)
        print(f"  ✓ Added '{uid}'")


def do_update():
    uid = _inp("  User ID: ")
    if not pm.user_exists(uid):
        print(f"  [ERROR] '{uid}' not found."); return
    changes = {}
    for field, label in [("name","Name"),("age","Age"),("city","City"),
                          ("profession","Job"),("bio","Bio")]:
        val = _inp(f"  {label} (blank=skip): ")
        if val:
            changes[field] = int(val) if field == "age" else val
    ints = _inp("  Interests (blank=skip): ")
    if ints:
        changes["interests"] = [x.strip() for x in ints.split(",")]
    if changes:
        pm.update_user_profile(uid, **changes)
        print("  ✓ Updated")


def do_bfs():
    src = _inp("  From: ")
    dst = _inp("  To  : ")
    print_bfs_result(src, dst, bfs_shortest_path(graph.get_adjacency(), src, dst))


def do_dfs():
    start = _inp("  Start: ")
    try:
        depth = int(_inp("  Depth: "))
    except ValueError:
        print("  [ERROR] Depth must be integer."); return
    print_dfs_result(start, depth, dfs_friends_of_friends(graph.get_adjacency(), start, depth))


def do_suggest():
    uid  = _inp("  User ID: ")
    algo = _inp("  Sort (merge/insertion): ").lower()
    if algo not in ("merge", "insertion"):
        algo = "merge"
    sugs = get_top_suggestions(uid, pm, graph.get_adjacency(), top_n=5, algo=algo)
    print(f"\n  Suggestions for '{uid}':")
    if not sugs:
        print("  None found.")
        return
    for i, (score, cid) in enumerate(sugs, 1):
        nm = pm.users.get(cid, {}).get("name", "?")
        print(f"  {i}. {cid} ({nm}) — {score} common interests")


def main():
    print("\n" + "="*58)
    print("   Social Network Explorer  |  ETCCDS202")
    print("="*58)

    if _inp("\n  Load demo data? (y/n): ").lower() == "y":
        load_demo()

    actions = {
        "1": do_add_user,
        "2": lambda: pm.display_profile(_inp("  User ID: ")),
        "3": do_update,
        "4": lambda: graph.add_friendship(_inp("  User 1: "), _inp("  User 2: "), pm),
        "5": lambda: graph.remove_friendship(_inp("  User 1: "), _inp("  User 2: ")),
        "6": lambda: graph.display_connections(_inp("  User ID: ")),
        "7": do_bfs,
        "8": do_dfs,
        "9": do_suggest,
        "10": pm.display_all_profiles,
        "11": graph.display_full_graph,
    }

    while True:
        show_menu()
        opt = _inp("  Option: ")
        if opt == "0":
            print("\n  Bye!\n"); break
        fn = actions.get(opt)
        if fn:
            fn()
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
