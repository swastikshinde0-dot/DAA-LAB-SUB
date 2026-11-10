"""
Lab Task 2 - Part 1: Trace It Yourself
Given list: 8, 3, 15, 6, 2

1. Find the largest number by checking one number at a time (comparisons counted).
2. Sort the list from smallest to largest (Bubble Sort), showing steps.
"""


def find_largest(a):
    """Scan the list once, keeping track of the max seen so far."""
    max_val = a[0]
    comparisons = 0
    print(f"i = 0, A[i] = {a[0]}, max = {max_val} (starting value, no comparison yet)")
    for i in range(1, len(a)):
        comparisons += 1
        if a[i] > max_val:
            max_val = a[i]
        print(f"i = {i}, A[i] = {a[i]}, max = {max_val}, comparisons = {comparisons}")
    return max_val, comparisons


def bubble_sort(a):
    """Classic bubble sort, printing each swap as a step."""
    arr = a[:]
    n = len(arr)
    step = 1
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                print(f"Step {step}: swapped {arr[j+1]} and {arr[j]} -> {arr}")
                step += 1
    return arr


if __name__ == "__main__":
    data = [8, 3, 15, 6, 2]

    print("Input:", data)
    print("\n--- Finding largest ---")
    largest, comps = find_largest(data)
    print(f"\nOutput (largest): {largest}")
    print(f"Total comparisons made: {comps}")

    print("\n--- Sorting (Bubble Sort) ---")
    sorted_list = bubble_sort(data)
    print(f"\nOutput (sorted): {sorted_list}")