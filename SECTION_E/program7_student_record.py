"""
Program 7: Student Record Manager
Manages student records (roll number, name, marks).
Features:
- Sort records by roll number, name, or marks using any of the 6 algorithms (Bubble, Selection, Insertion, Merge, Quick, Heap).
- Search for a student by roll number using Binary Search (verifying dataset is sorted by roll number).
- Benchmark all 6 algorithms on the same dataset and print a comparative performance report (fastest vs slowest).
"""

import time
import sys
import copy

# Ensure recursion depth for quick sort
sys.setrecursionlimit(10000)

# Predefined dataset of student records
INITIAL_RECORDS = [
    {"roll_no": 105, "name": "Rahul Sharma", "marks": 82.5},
    {"roll_no": 102, "name": "Ananya Patel", "marks": 94.0},
    {"roll_no": 110, "name": "Devansh Gupta", "marks": 71.0},
    {"roll_no": 101, "name": "Aarav Mehta", "marks": 88.5},
    {"roll_no": 108, "name": "Ishita Verma", "marks": 91.0},
    {"roll_no": 103, "name": "Kavya Singh", "marks": 78.0},
    {"roll_no": 107, "name": "Manish Nair", "marks": 85.0},
    {"roll_no": 104, "name": "Pooja Joshi", "marks": 96.5},
    {"roll_no": 109, "name": "Rohan Bhatia", "marks": 69.0},
    {"roll_no": 106, "name": "Simran Kaur", "marks": 89.0},
    {"roll_no": 112, "name": "Tanmay Deshmukh", "marks": 74.5},
    {"roll_no": 111, "name": "Zoya Khan", "marks": 93.0},
]


# =====================================================================
# Sorting Algorithms supporting key extraction
# =====================================================================

def bubble_sort(arr, key=lambda x: x):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if key(arr[j]) > key(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr, key=lambda x: x):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if key(arr[j]) < key(arr[min_idx]):
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr, key=lambda x: x):
    n = len(arr)
    for i in range(1, n):
        item = arr[i]
        val = key(item)
        j = i - 1
        while j >= 0 and key(arr[j]) > val:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = item
    return arr


def merge_sort(arr, key=lambda x: x):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort(left, key=key)
        merge_sort(right, key=key)

        i = j = k = 0
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
    return arr


def quick_sort(arr, low=0, high=None, key=lambda x: x):
    if high is None:
        high = len(arr) - 1

    if low < high:
        # Lomuto partition scheme using last element as pivot
        pivot_val = key(arr[high])
        i = low - 1
        for j in range(low, high):
            if key(arr[j]) <= pivot_val:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        pi = i + 1

        quick_sort(arr, low, pi - 1, key=key)
        quick_sort(arr, pi + 1, high, key=key)
    return arr


def _heapify(arr, n, i, key):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and key(arr[left]) > key(arr[largest]):
        largest = left
    if right < n and key(arr[right]) > key(arr[largest]):
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify(arr, n, largest, key)


def heap_sort(arr, key=lambda x: x):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i, key)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(arr, i, 0, key)
    return arr


ALGORITHMS = {
    1: ("Bubble Sort", bubble_sort),
    2: ("Selection Sort", selection_sort),
    3: ("Insertion Sort", insertion_sort),
    4: ("Merge Sort", merge_sort),
    5: ("Quick Sort", quick_sort),
    6: ("Heap Sort", heap_sort),
}

FIELDS = {
    1: ("Roll Number", lambda s: s["roll_no"]),
    2: ("Name", lambda s: s["name"].lower()),
    3: ("Marks", lambda s: s["marks"]),
}


# =====================================================================
# Binary Search on Student Records by Roll Number
# =====================================================================

def is_sorted_by_roll(records):
    """Checks if the records are currently sorted by roll_no in ascending order."""
    for i in range(len(records) - 1):
        if records[i]["roll_no"] > records[i + 1]["roll_no"]:
            return False
    return True


def binary_search_student(records, target_roll):
    """
    Searches for a student by roll number using iterative binary search.
    Requires records to be sorted by roll_no.
    Returns: (record, index, comparisons) or (None, -1, comparisons).
    """
    low = 0
    high = len(records) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        mid_roll = records[mid]["roll_no"]

        if mid_roll == target_roll:
            return records[mid], mid, comparisons
        elif mid_roll < target_roll:
            low = mid + 1
        else:
            high = mid - 1

    return None, -1, comparisons


# =====================================================================
# Comparative Performance Benchmark
# =====================================================================

def run_performance_report(records, repeat=200):
    """
    Times all 6 algorithms sorting copies of the same dataset.
    Runs multiple repetitions to obtain stable microsecond-level timing.
    Prints fastest, slowest, and ratio report.
    """
    print("\n" + "=" * 65)
    print("COMPARATIVE PERFORMANCE REPORT ON STUDENT RECORDS DATASET")
    print(f"Dataset Size: {len(records)} records | Repetitions: {repeat}")
    print("=" * 65)

    timings = {}
    for code, (name, fn) in ALGORITHMS.items():
        total_time = 0.0
        for _ in range(repeat):
            dataset_copy = copy.deepcopy(records)
            start = time.perf_counter()
            fn(dataset_copy, key=lambda s: s["roll_no"])
            total_time += time.perf_counter() - start
        avg_time_us = (total_time / repeat) * 1e6  # Microseconds
        timings[name] = avg_time_us

    sorted_timings = sorted(timings.items(), key=lambda x: x[1])
    fastest_name, fastest_time = sorted_timings[0]
    slowest_name, slowest_time = sorted_timings[-1]

    print(f"{'Algorithm':<18} | {'Average Time (microseconds)':>26}")
    print("-" * 50)
    for name, t in sorted_timings:
        print(f"{name:<18} | {t:>26.2f} µs")

    print("-" * 50)
    diff = slowest_time - fastest_time
    ratio = slowest_time / fastest_time if fastest_time > 0 else 1.0
    print(f"Fastest Algorithm : {fastest_name} ({fastest_time:.2f} µs)")
    print(f"Slowest Algorithm : {slowest_name} ({slowest_time:.2f} µs)")
    print(f"Difference        : {diff:.2f} µs ({slowest_name} is {ratio:.2f}x slower than {fastest_name})")
    print("=" * 65)


def print_records(records, title="Student Records"):
    print(f"\n--- {title} (Total: {len(records)}) ---")
    print(f"{'Roll No':<10} | {'Name':<22} | {'Marks':>6}")
    print("-" * 44)
    for s in records:
        print(f"{s['roll_no']:<10} | {s['name']:<22} | {s['marks']:>6.1f}")


# =====================================================================
# Demonstration & Interactive Interface
# =====================================================================

def run_demo():
    print("================================================================")
    print("       STUDENT RECORD MANAGER - DEMONSTRATION MODE             ")
    print("================================================================")
    current_records = copy.deepcopy(INITIAL_RECORDS)
    print_records(current_records, "Initial Unsorted Records")

    # 1. Sort by Marks (Descending / Ascending) using Merge Sort
    print("\n[Step 1] Sorting by Marks using Merge Sort...")
    merge_sort(current_records, key=lambda s: s["marks"])
    print_records(current_records, "Records Sorted by Marks (Ascending)")

    # 2. Sort by Name using Quick Sort
    print("\n[Step 2] Sorting by Name using Quick Sort...")
    quick_sort(current_records, key=lambda s: s["name"].lower())
    print_records(current_records, "Records Sorted by Name")

    # 3. Sort by Roll Number using Insertion Sort
    print("\n[Step 3] Sorting by Roll Number using Insertion Sort (required for Binary Search)...")
    insertion_sort(current_records, key=lambda s: s["roll_no"])
    print_records(current_records, "Records Sorted by Roll Number")

    # 4. Binary Search by Roll Number
    print("\n[Step 4] Binary Search for Student by Roll Number:")
    for search_roll in [106, 115]:
        print(f"\nSearching for Roll Number: {search_roll}")
        student, idx, comps = binary_search_student(current_records, search_roll)
        if student:
            print(f"  FOUND at index {idx} in {comps} comparison(s): {student['name']}, Marks: {student['marks']}")
        else:
            print(f"  NOT FOUND after {comps} comparison(s).")

    # 5. Comparative Performance Report
    print("\n[Step 5] Running Comparative Performance Benchmark on all 6 algorithms...")
    run_performance_report(INITIAL_RECORDS)


def interactive_menu():
    records = copy.deepcopy(INITIAL_RECORDS)
    while True:
        print("\n" + "=" * 50)
        print("          STUDENT RECORD MANAGER MENU            ")
        print("=" * 50)
        print("1. Display all student records")
        print("2. Sort records (Choose field & algorithm)")
        print("3. Search student by Roll Number (Binary Search)")
        print("4. Run Comparative Performance Report")
        print("5. Run Full Automated Demonstration")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            print_records(records)
        elif choice == "2":
            print("\nSelect Field to Sort By:")
            print("1. Roll Number\n2. Name\n3. Marks")
            f_choice = int(input("Field choice (1-3): ").strip())
            field_name, key_fn = FIELDS.get(f_choice, FIELDS[1])

            print("\nSelect Algorithm:")
            for code, (name, _) in ALGORITHMS.items():
                print(f"{code}. {name}")
            a_choice = int(input("Algorithm choice (1-6): ").strip())
            algo_name, sort_fn = ALGORITHMS.get(a_choice, ALGORITHMS[1])

            sort_fn(records, key=key_fn)
            print(f"\nRecords successfully sorted by {field_name} using {algo_name}!")
            print_records(records, f"Sorted by {field_name}")

        elif choice == "3":
            if not is_sorted_by_roll(records):
                print("\n[NOTICE] Records are not currently sorted by Roll Number.")
                print("Binary Search requires sorted order. Sorting by Roll Number now...")
                quick_sort(records, key=lambda s: s["roll_no"])

            roll = int(input("\nEnter Roll Number to search: ").strip())
            student, idx, comps = binary_search_student(records, roll)
            if student:
                print(f"\n[FOUND] Index: {idx} | Comparisons: {comps}")
                print(f"Details: Roll No: {student['roll_no']}, Name: {student['name']}, Marks: {student['marks']}")
            else:
                print(f"\n[NOT FOUND] Roll Number {roll} not found after {comps} comparisons.")

        elif choice == "4":
            run_performance_report(records)
        elif choice == "5":
            run_demo()
        elif choice == "6":
            print("Exiting Student Record Manager.")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_menu()
    else:
        run_demo()