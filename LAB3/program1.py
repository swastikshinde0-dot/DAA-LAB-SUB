"""
Program 1: Bubble Sort, Selection Sort, Insertion Sort
Implementation of elementary comparison-based sorting algorithms.
Each algorithm is a standalone function that sorts in-place and returns the sorted list.
"""

def bubble_sort(arr, verbose=False):
    """
    Sorts a list in-place using Bubble Sort.
    Repeatedly compares adjacent elements and swaps them if they are in the wrong order.
    """
    n = len(arr)
    if verbose:
        print(f"Initial Array: {arr}")
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if verbose:
            print(f"Pass {i + 1}: {arr}")
        if not swapped:
            if verbose:
                print("No swaps in this pass; array is already sorted. Early exit.")
            break
    return arr


def selection_sort(arr, verbose=False):
    """
    Sorts a list in-place using Selection Sort.
    Repeatedly finds the minimum element from the unsorted part and swaps it with the beginning.
    """
    n = len(arr)
    if verbose:
        print(f"Initial Array: {arr}")
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if verbose:
            print(f"Step {i + 1} (min placed at index {i}): {arr}")
    return arr


def insertion_sort(arr, verbose=False):
    """
    Sorts a list in-place using Insertion Sort.
    Builds the sorted portion one element at a time by inserting each element
    into its correct position within the sorted sublist.
    """
    n = len(arr)
    if verbose:
        print(f"Initial Array: {arr}")
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        if verbose:
            print(f"Step {i} (inserted {key}): {arr}")
    return arr


if __name__ == "__main__":
    sample = [64, 34, 25, 12, 22, 11, 90]
    print("=" * 60)
    print("TESTING BUBBLE SORT")
    print("=" * 60)
    arr_bubble = list(sample)
    bubble_sort(arr_bubble, verbose=True)
    print(f"Final Sorted Array: {arr_bubble}\n")

    print("=" * 60)
    print("TESTING SELECTION SORT")
    print("=" * 60)
    arr_selection = list(sample)
    selection_sort(arr_selection, verbose=True)
    print(f"Final Sorted Array: {arr_selection}\n")

    print("=" * 60)
    print("TESTING INSERTION SORT")
    print("=" * 60)
    arr_insertion = list(sample)
    insertion_sort(arr_insertion, verbose=True)
    print(f"Final Sorted Array: {arr_insertion}\n")
