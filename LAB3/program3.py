"""
Program 3: Radix Sort
Implementation of Radix Sort for non-negative integers using the Least Significant Digit (LSD) approach.
Uses a stable Counting Sort helper function on a single digit place, called repeatedly for each digit position.
"""

def counting_sort_by_digit(arr, exp, verbose=False):
    """
    Helper function: Performs stable Counting Sort on arr according to the digit
    at position represented by exp (1s place, 10s place, 100s place, etc.).
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # Count occurrences of each digit at (arr[i] // exp) % 10
    for i in range(n):
        digit = (arr[i] // exp) % 10
        count[digit] += 1

    # Compute prefix sums so count[i] contains actual position of this digit in output
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build output array stably from right to left
    for i in range(n - 1, -1, -1):
        digit = (arr[i] // exp) % 10
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    # Copy output back to original array
    for i in range(n):
        arr[i] = output[i]

    if verbose:
        place_name = {1: "ones", 10: "tens", 100: "hundreds", 1000: "thousands"}.get(exp, f"10^{len(str(exp))-1}")
        print(f"After sorting by {place_name} digit (exp={exp}): {arr}")


def radix_sort(arr, verbose=False):
    """
    Sorts a list of non-negative integers in-place using Radix Sort (LSD approach).
    Finds the maximum value to determine the number of digits, then calls counting_sort_by_digit.
    """
    if not arr:
        return arr

    max_val = max(arr)

    # Do counting sort for every digit. exp is 10^i where i is current digit number
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp, verbose=verbose)
        exp *= 10

    return arr


if __name__ == "__main__":
    print("=" * 60)
    print("TESTING RADIX SORT (LSD APPROACH)")
    print("=" * 60)

    sample = [170, 45, 75, 90, 802, 24, 2, 66]
    print(f"Initial Array: {sample}\n")

    arr_radix = list(sample)
    radix_sort(arr_radix, verbose=True)

    print(f"\nFinal Sorted Array: {arr_radix}")