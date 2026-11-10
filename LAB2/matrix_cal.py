"""
Program 4: Matrix Calculator (menu-driven)
Supports addition, multiplication, transpose, and determinant calculation
for matrices entered by the user.
"""


def add_matrices(a, b):
    rows_a, cols_a = len(a), (len(a[0]) if a else 0)
    rows_b, cols_b = len(b), (len(b[0]) if b else 0)
    if rows_a != rows_b or cols_a != cols_b:
        raise ValueError(
            f"Cannot add matrices of size {rows_a}x{cols_a} and {rows_b}x{cols_b}"
        )
    return [[a[r][c] + b[r][c] for c in range(cols_a)] for r in range(rows_a)]


def multiply_matrices(a, b):
    rows_a, cols_a = len(a), (len(a[0]) if a else 0)
    rows_b, cols_b = len(b), (len(b[0]) if b else 0)
    if cols_a != rows_b:
        raise ValueError(
            f"Cannot multiply {rows_a}x{cols_a} by {rows_b}x{cols_b}: "
            f"columns of A must match rows of B"
        )
    result = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            result[i][j] = sum(a[i][k] * b[k][j] for k in range(cols_a))
    return result


def transpose(matrix):
    if not matrix:
        return []
    rows, cols = len(matrix), len(matrix[0])
    return [[matrix[r][c] for r in range(rows)] for c in range(cols)]


def is_square(matrix):
    return len(matrix) > 0 and all(len(row) == len(matrix) for row in matrix)


def determinant(matrix):
    """Recursive cofactor expansion. Handles any n x n matrix, so it covers
    the required 2x2 and 3x3 cases directly (the assignment only requires
    those two sizes; the general recursive case is an optional extension)."""
    if not is_square(matrix):
        raise ValueError("Determinant is only defined for square matrices")

    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    sign = 1
    for col in range(n):
        minor = [row[:col] + row[col + 1:] for row in matrix[1:]]
        det += sign * matrix[0][col] * determinant(minor)
        sign *= -1
    return det


def print_matrix(matrix, label="Result"):
    print(f"{label}:")
    if not matrix:
        print("  (empty)")
        return
    for row in matrix:
        print(" ", row)


def read_matrix(label="Matrix"):
    rows = int(input(f"{label} -- number of rows: "))
    cols = int(input(f"{label} -- number of columns: "))
    matrix = []
    for r in range(rows):
        row = [int(x) for x in input(f"  Row {r} ({cols} space-separated values): ").split()]
        if len(row) != cols:
            raise ValueError(f"Expected {cols} values, got {len(row)}")
        matrix.append(row)
    return matrix


def menu():
    while True:
        print("\n--- Matrix Calculator ---")
        print("1. Add two matrices")
        print("2. Multiply two matrices")
        print("3. Transpose a matrix")
        print("4. Determinant of a matrix")
        print("5. Exit")
        choice = input("Choose an operation: ").strip()

        try:
            if choice == "1":
                a = read_matrix("Matrix A")
                b = read_matrix("Matrix B")
                print_matrix(add_matrices(a, b), "A + B")

            elif choice == "2":
                a = read_matrix("Matrix A")
                b = read_matrix("Matrix B")
                print_matrix(multiply_matrices(a, b), "A x B")

            elif choice == "3":
                m = read_matrix("Matrix")
                print_matrix(transpose(m), "Transpose")

            elif choice == "4":
                m = read_matrix("Matrix")
                if not is_square(m):
                    print("Error: determinant requires a square matrix")
                else:
                    print(f"Determinant: {determinant(m)}")

            elif choice == "5":
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
