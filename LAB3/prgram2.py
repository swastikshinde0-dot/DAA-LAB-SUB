"""
Program 2: Merge Sort, Quick Sort, Heap Sort
Implementation of divide-and-conquer and heap-based O(n log n) average time sorting algorithms.
Each algorithm is a standalone function that sorts in-place and returns the sorted list.
"""
import sys

# Increase recursion depth limit to support quicksort on deep recursive calls (e.g., sorted arrays)
sys.setrecursionlimit(10000)


def merge_sort(arr):
    """
    Sorts a list in-place using Merge Sort (Divide and Conquer).
    Splits the array into two halves, recursively sorts both halves,
    and merges them back in sorted order.
    """
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
    """
    Lomuto partition scheme using the LAST element as the pivot.
    PIVOT SELECTION STRATEGY: Last element (arr[high]).
    Rearranges elements such that all elements <= pivot are placed before it,
    and all elements > pivot are placed after it.
    """
    pivot = arr[high]  # Pivot strategy: LAST element
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort(arr, low=0, high=None):
    """
    Sorts a list in-place using Quick Sort.
    PIVOT SELECTION STRATEGY: Last element of the current partition range (arr[high]).
    Partitions around the pivot and recursively sorts subarrays.
    """
    if high is None:
        high = len(arr) - 1

    # Use tail recursion optimization or standard recursion for range
    if low < high:
        pi = _partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

    return arr


def _heapify(arr, n, i):
    """
    Maintains the max-heap property for a subtree rooted at index i in an array of size n.
    """
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
    """
    Sorts a list in-place using Heap Sort.
    Converts the array into a max-heap, then repeatedly extracts the maximum element
    to the end of the array and heapifies the remaining heap.
    """
    n = len(arr)

    # Build max heap (rearrange array)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(arr, n, i)

    # One by one extract elements from heap
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]  # Move current root to end
        _heapify(arr, i, 0)  # Call max heapify on reduced heap

    return arr


if __name__ == "__main__":
    sample = [64, 34, 25, 12, 22, 11, 90]
    print("=" * 60)
    print("TESTING ADVANCED SORTS ON SAMPLE:", sample)
    print("=" * 60)

    arr_merge = list(sample)
    merge_sort(arr_merge)
    print(f"Merge Sort Result: {arr_merge}")

    arr_quick = list(sample)
    quick_sort(arr_quick)
    print(f"Quick Sort Result (Pivot: Last Element): {arr_quick}")

    arr_heap = list(sample)
    heap_sort(arr_heap)
    print(f"Heap Sort Result:  {arr_heap}")