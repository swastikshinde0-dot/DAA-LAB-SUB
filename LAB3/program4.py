"""
Program 4: Binary Search
Implementation of iterative Binary Search on a sorted array.
Returns the index of the target if found, or -1 if not found.
"""

def binary_search(arr, target, verbose=False):
    """
    Performs iterative binary search on a sorted array.
    Returns:
        int: Index of target in arr, or -1 if target is not present.
    """
    low = 0
    high = len(arr) - 1
    step = 1

    if verbose:
        print(f"Searching for target {target} in array of length {len(arr)}...")

    while low <= high:
        mid = (low + high) // 2
        mid_val = arr[mid]

        if verbose:
            print(f"  Step {step}: low={low} (val={arr[low]}), high={high} (val={arr[high]}), mid={mid} (val={mid_val})")
        step += 1

        if mid_val == target:
            if verbose:
                print(f"  Target {target} found at index {mid}!")
            return mid
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    if verbose:
        print(f"  Target {target} not found in array (returning -1).")
    return -1


if __name__ == "__main__":
    sorted_array = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
    print("=" * 60)
    print("TESTING ITERATIVE BINARY SEARCH")
    print(f"Array: {sorted_array}")
    print("=" * 60)

    # Test 1: Target that exists
    target_existing = 23
    print(f"\nTest 1: Target that exists ({target_existing})")
    idx1 = binary_search(sorted_array, target_existing, verbose=True)
    print(f"Result: Index = {idx1}")

    # Test 2: Target that does not exist
    target_missing = 50
    print(f"\nTest 2: Target that does not exist ({target_missing})")
    idx2 = binary_search(sorted_array, target_missing, verbose=True)
    print(f"Result: Index = {idx2}")

    # Test 3: Boundary element (first element)
    print(f"\nTest 3: First element ({sorted_array[0]})")
    idx3 = binary_search(sorted_array, sorted_array[0], verbose=True)
    print(f"Result: Index = {idx3}")