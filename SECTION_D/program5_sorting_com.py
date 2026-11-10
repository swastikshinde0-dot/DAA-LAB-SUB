"""
Program 5: Empirical Timing Analysis of Sorting Algorithms
Generates random, already-sorted, and reverse-sorted arrays of sizes n = 100, 500, 1000, 2000.
Times Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, Quick Sort, and Heap Sort.
Outputs a formatted results table and writes raw timing data to timing_results.csv.
"""

import time
import random
import csv
import sys
import os

# Ensure recursion depth is sufficient for Quick Sort on sorted inputs
sys.setrecursionlimit(15000)


# =====================================================================
# Standalone Sorting Algorithm Implementations (from Programs 1 & 2)
# =====================================================================

def bubble_sort(arr):
    """Sorts list in-place using Bubble Sort with early exit optimization."""
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr):
    """Sorts list in-place using Selection Sort."""
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr):
    """Sorts list in-place using Insertion Sort."""
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(arr):
    """Sorts list in-place using Merge Sort (Divide and Conquer)."""
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr


def _partition(arr, low, high):
    """Lomuto partition scheme using the last element as pivot."""
    pivot = arr[high]  # Pivot: LAST element
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low=0, high=None):
    """Sorts list in-place using Quick Sort with last element pivot."""
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = _partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    return arr


def _heapify(arr, n, i):
    """Maintains max-heap property for subtree rooted at index i."""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest)


def heap_sort(arr):
    """Sorts list in-place using Heap Sort."""
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0)
    return arr


# =====================================================================
# Array Generation & Benchmarking Logic
# =====================================================================

def generate_input_array(n, input_type):
    """
    Generates an array of size n based on input_type:
    - 'random': randomly shuffled integers
    - 'sorted': already sorted in ascending order
    - 'reverse_sorted': sorted in descending order
    """
    if input_type == "random":
        return [random.randint(1, n * 10) for _ in range(n)]
    elif input_type == "sorted":
        return list(range(1, n + 1))
    elif input_type == "reverse_sorted":
        return list(range(n, 0, -1))
    else:
        raise ValueError(f"Unknown input type: {input_type}")


def time_algorithm(sort_fn, arr):
    """
    Times the execution of a sorting algorithm on a copy of arr.
    Returns elapsed time in seconds.
    """
    arr_copy = list(arr)
    start_time = time.perf_counter()
    sort_fn(arr_copy)
    end_time = time.perf_counter()
    return end_time - start_time


def run_benchmarks(sizes=[100, 500, 1000, 2000], seed=42):
    """
    Runs the full empirical timing experiment.
    Returns a list of result dictionaries.
    """
    random.seed(seed)
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Quick Sort", quick_sort),
        ("Heap Sort", heap_sort),
    ]
    input_types = ["random", "sorted", "reverse_sorted"]
    results = []

    for n in sizes:
        for itype in input_types:
            base_arr = generate_input_array(n, itype)
            for name, fn in algorithms:
                elapsed = time_algorithm(fn, base_arr)
                results.append({
                    "Algorithm": name,
                    "Input_Type": itype,
                    "N": n,
                    "Time_Seconds": elapsed,
                    "Time_MS": elapsed * 1000.0,
                })

    return results


def print_results_table(results):
    """Prints a formatted ASCII table of the timing results."""
    header = f"{'Algorithm':<16} | {'Input Type':<15} | {'N':>6} | {'Time (s)':>12} | {'Time (ms)':>12}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r['Algorithm']:<16} | {r['Input_Type']:<15} | {r['N']:>6} | {r['Time_Seconds']:>12.6f} | {r['Time_MS']:>12.3f}")


def save_results_csv(results, filepath="timing_results.csv"):
    """Saves timing results to a CSV file."""
    with open(filepath, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Algorithm", "Input_Type", "N", "Time_Seconds", "Time_MS"])
        writer.writeheader()
        writer.writerows(results)
    print(f"\n[INFO] Raw timing data saved successfully to '{filepath}'.")


if __name__ == "__main__":
    print("=" * 70)
    print("RUNNING EMPIRICAL TIMING ANALYSIS (PROGRAM 5)")
    print("=" * 70)
    test_sizes = [100, 500, 1000, 2000]
    results = run_benchmarks(sizes=test_sizes)
    print_results_table(results)

    # Save CSV in the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "timing_results.csv")
    save_results_csv(results, csv_path)
