"""
Program 3: Sparse Matrix Representation and Operations
Converts between full and sparse (triple) representations, and adds two
matrices while they remain in sparse form.

A sparse matrix is represented here as a dict:
    {"rows": m, "cols": n, "triples": [(r, c, value), ...]}
where triples are non-zero entries listed in row-major order.
"""


def to_sparse(matrix):
    """Convert a full 2D list into its sparse triple representation."""
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    triples = []
    for r in range(rows):
        if len(matrix[r]) != cols:
            raise ValueError(f"Row {r} has length {len(matrix[r])}, expected {cols}")
        for c in range(cols):
            if matrix[r][c] != 0:
                triples.append((r, c, matrix[r][c]))
    return {"rows": rows, "cols": cols, "triples": triples}


def from_sparse(sparse):
    """Reconstruct the full 2D matrix from a sparse triple representation."""
    rows, cols = sparse["rows"], sparse["cols"]
    matrix = [[0] * cols for _ in range(rows)]
    for r, c, value in sparse["triples"]:
        if r < 0 or r >= rows or c < 0 or c >= cols:
            raise IndexError(f"Triple ({r}, {c}, {value}) out of bounds for a {rows}x{cols} matrix")
        matrix[r][c] = value
    return matrix


def add_sparse(sparse_a, sparse_b):
    """Add two matrices that are both already in sparse form, producing a
    sparse result -- without reconstructing either input as a full matrix.

    Both triple lists are sorted in row-major order (guaranteed by
    to_sparse). This walks both lists with two pointers, merging entries
    that share a (row, col) position and copying over entries that appear
    in only one matrix -- the same merge idea used in merge sort.
    """
    if sparse_a["rows"] != sparse_b["rows"] or sparse_a["cols"] != sparse_b["cols"]:
        raise ValueError(
            f"Dimension mismatch: {sparse_a['rows']}x{sparse_a['cols']} "
            f"vs {sparse_b['rows']}x{sparse_b['cols']}"
        )

    triples_a = sparse_a["triples"]
    triples_b = sparse_b["triples"]
    i, j = 0, 0
    result_triples = []

    while i < len(triples_a) and j < len(triples_b):
        ra, ca, va = triples_a[i]
        rb, cb, vb = triples_b[j]
        pos_a = (ra, ca)
        pos_b = (rb, cb)

        if pos_a < pos_b:
            result_triples.append((ra, ca, va))
            i += 1
        elif pos_a > pos_b:
            result_triples.append((rb, cb, vb))
            j += 1
        else:  # same position in both matrices -- add the values
            total = va + vb
            if total != 0:
                result_triples.append((ra, ca, total))
            i += 1
            j += 1

    # copy over whichever list still has entries left
    while i < len(triples_a):
        result_triples.append(triples_a[i])
        i += 1
    while j < len(triples_b):
        result_triples.append(triples_b[j])
        j += 1

    return {"rows": sparse_a["rows"], "cols": sparse_a["cols"], "triples": result_triples}


def print_sparse(sparse, label="Sparse form"):
    print(f"{label} (rows={sparse['rows']}, cols={sparse['cols']}, non-zero={len(sparse['triples'])}):")
    if not sparse["triples"]:
        print("  (no non-zero entries)")
    for r, c, v in sparse["triples"]:
        print(f"  ({r}, {c}, {v})")


def print_matrix(matrix, label="Full form"):
    print(f"{label}:")
    if not matrix:
        print("  (empty)")
        return
    for row in matrix:
        print(" ", row)


def read_matrix():
    rows = int(input("Number of rows: "))
    cols = int(input("Number of columns: "))
    matrix = []
    print(f"Enter {rows} rows, each with {cols} space-separated values:")
    for r in range(rows):
        row = [int(x) for x in input(f"Row {r}: ").split()]
        if len(row) != cols:
            raise ValueError(f"Expected {cols} values, got {len(row)}")
        matrix.append(row)
    return matrix


def menu():
    while True:
        print("\n--- Sparse Matrix Operations ---")
        print("1. Convert a matrix to sparse form and back")
        print("2. Add two matrices in sparse form")
        print("3. Exit")
        choice = input("Choose an operation: ").strip()

        try:
            if choice == "1":
                matrix = read_matrix()
                sparse = to_sparse(matrix)
                print_matrix(matrix, "Original full form")
                print_sparse(sparse)
                rebuilt = from_sparse(sparse)
                print_matrix(rebuilt, "Reconstructed full form")
                print("Matches original:", rebuilt == matrix)

            elif choice == "2":
                print("Matrix A:")
                sparse_a = to_sparse(read_matrix())
                print("Matrix B:")
                sparse_b = to_sparse(read_matrix())
                result = add_sparse(sparse_a, sparse_b)
                print_sparse(sparse_a, "Matrix A (sparse)")
                print_sparse(sparse_b, "Matrix B (sparse)")
                print_sparse(result, "A + B (sparse)")
                print_matrix(from_sparse(result), "A + B (full, for verification)")

            elif choice == "3":
                print("Exiting.")
                break

            else:
                print("Invalid choice, try again.")

        except ValueError as e:
            print(f"Invalid input: {e}")
        except IndexError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu()