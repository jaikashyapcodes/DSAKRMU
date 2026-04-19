"""
sorting.py - sorting algorithms + friend suggestion logic

Recommendation idea:
  Build an inverted index mapping each interest to the users who have it.
  For a given user, look up their interests in the index to collect candidates.
  Count how many interests each candidate shares with the user (the score).
  Sort candidates by score descending and return the top results.
  Hashing makes the index lookup fast; sorting ranks the output cleanly.
"""


def insertion_sort(items):
    arr = list(items)
    for i in range(1, len(arr)):
        cur = arr[i]
        j = i - 1
        while j >= 0 and arr[j][0] < cur[0]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = cur
    return arr


def merge_sort(items):
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    L = merge_sort(items[:mid])
    R = merge_sort(items[mid:])
    res, i, j = [], 0, 0
    while i < len(L) and j < len(R):
        if L[i][0] >= R[j][0]:
            res.append(L[i]); i += 1
        else:
            res.append(R[j]); j += 1
    res.extend(L[i:])
    res.extend(R[j:])
    return res


def build_interest_index(pm):
    idx = {}
    for uid in pm.all_user_ids():
        p = pm.users.get(uid)
        if p:
            for interest in p["interests"]:
                idx.setdefault(interest.lower(), []).append(uid)
    return idx


def compute_scores(uid, pm, adj, idx):
    p = pm.users.get(uid)
    if not p:
        return []
    my_interests = set(i.lower() for i in p["interests"])
    exclude = set(adj.get(uid, [])) | {uid}
    scores = {}
    for interest in my_interests:
        for candidate in idx.get(interest, []):
            if candidate not in exclude:
                scores[candidate] = scores.get(candidate, 0) + 1
    return [(s, u) for u, s in scores.items()]


def get_top_suggestions(uid, pm, adj, top_n=5, algo="merge"):
    idx = build_interest_index(pm)
    raw = compute_scores(uid, pm, adj, idx)
    ranked = insertion_sort(raw) if algo == "insertion" else merge_sort(raw)
    return ranked[:top_n]


def compare_sorts_demo(items):
    import time
    t0 = time.perf_counter(); r1 = insertion_sort(items); t1 = time.perf_counter()
    t2 = time.perf_counter(); r2 = merge_sort(items);     t3 = time.perf_counter()
    print(f"\n  Sort comparison ({len(items)} items):")
    print(f"  Insertion : {(t1-t0)*1e6:.2f} µs  → {r1[:3]}")
    print(f"  Merge     : {(t3-t2)*1e6:.2f} µs  → {r2[:3]}")
    print(f"  Same result: {r1 == r2}")
