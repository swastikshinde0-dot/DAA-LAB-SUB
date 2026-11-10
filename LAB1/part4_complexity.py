"""
Lab Task 2 - Part 4: Count the Steps

Single loop:
    FOR i = 1 to 5
        PRINT i

Nested loop:
    FOR i = 1 to 5
        FOR j = 1 to 5
            PRINT i, j

1. How many times does the single loop run (n = 5)?
2. If it ran from 1 to n, and n = 20, how many times will it run?
3. How many times does the inner PRINT run in total (n = 5)?
4. If both loops ran from 1 to n, and n = 10, how many times will PRINT run?
"""


def single_loop(n):
    """O(n): runs exactly n times."""
    count = 0
    for i in range(1, n + 1):
        count += 1
        print(f"PRINT {i}  (run #{count})")
    return count


def nested_loop(n):
    """O(n^2): inner PRINT runs n times for every outer i, so n * n total."""
    count = 0
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            count += 1
            print(f"PRINT {i}, {j}  (run #{count})")
    return count


if __name__ == "__main__":
    print("=== Single loop, n = 5 ===")
    total_single_5 = single_loop(5)
    print(f"\nSingle loop total runs (n=5): {total_single_5}")

    print("\n=== Single loop, n = 20 (count only) ===")
    print(f"Single loop total runs (n=20): {20} (formula: runs = n)")

    print("\n=== Nested loop, n = 5 ===")
    total_nested_5 = nested_loop(5)
    print(f"\nNested loop total PRINT calls (n=5): {total_nested_5}")

    print("\n=== Nested loop, n = 10 (count only) ===")
    n = 10
    print(f"Nested loop total PRINT calls (n=10): {n * n} (formula: runs = n^2)")