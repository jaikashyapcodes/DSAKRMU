import random
import time
import sys


def insertion_sort(arr):
    a = list(arr)
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(arr):
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)


def measure_time(sort_fn, arr):
    data = list(arr)
    start = time.perf_counter()
    sort_fn(data)
    end = time.perf_counter()
    return (end - start) * 1000


def generate_datasets():
    random.seed(42)
    sizes = [1000, 5000, 10000]
    datasets = {}
    for n in sizes:
        rand_list = random.sample(range(1, 100001), n)
        datasets[(n, "random")] = rand_list
        datasets[(n, "sorted")] = sorted(rand_list)
        datasets[(n, "reverse")] = sorted(rand_list, reverse=True)
    return datasets


def run_quick_sort(arr):
    data = list(arr)
    quick_sort(data, 0, len(data) - 1)
    return data


def main():
    sys.setrecursionlimit(50000)

    # correctness check
    test = [5, 2, 9, 1, 5, 6]
    expected = [1, 2, 5, 5, 6, 9]
    print("Correctness check: input =", test)
    print("Insertion sort:", insertion_sort(test), "->", "PASS" if insertion_sort(test) == expected else "FAIL")
    print("Merge sort:    ", merge_sort(test), "->", "PASS" if merge_sort(test) == expected else "FAIL")
    temp = list(test)
    quick_sort(temp, 0, len(temp) - 1)
    print("Quick sort:    ", temp, "->", "PASS" if temp == expected else "FAIL")
    print()

    datasets = generate_datasets()
    sizes = [1000, 5000, 10000]
    types = ["random", "sorted", "reverse"]

    print(f"{'n':<8} {'type':<10} {'insertion(ms)':>15} {'merge(ms)':>12} {'quick(ms)':>12}")
    print("-" * 60)

    for n in sizes:
        for t in types:
            arr = datasets[(n, t)]
            t_ins = measure_time(insertion_sort, arr)
            t_mrg = measure_time(merge_sort, arr)
            t_qck = measure_time(run_quick_sort, arr)
            print(f"{n:<8} {t:<10} {t_ins:>15.3f} {t_mrg:>12.3f} {t_qck:>12.3f}")
        print()


if __name__ == "__main__":
    main()
