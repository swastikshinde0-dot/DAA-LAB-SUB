"""
Program 2: 2D Array Operations
Supports insert row, delete row, search across a 2D list, and 90-degree
clockwise rotation.
"""


def insert_row(matrix, position, row):
    """Insert `row` at `position`. Row length must match the existing column
    count (any length is allowed if the matrix is currently empty)."""
    if matrix and len(row) != len(matrix[0]):
        raise ValueError(
            f"Row length {len(row)} does not match matrix column count {len(matrix[0])}"
        )
    if position < 0 or position > len(matrix):
        raise IndexError(
            f"Insert position {position} out of bounds for matrix with {len(matrix)} rows"
        )
    matrix.insert(position, list(row))
    return matrix


def delete_row(matrix, position):
    """Delete the row at `position`."""
    if len(matrix) == 0:
        raise IndexError("Cannot delete a row from an empty matrix")
    if position < 0 or position >= len(matrix):
        raise IndexError(
            f"Delete position {position} out of bounds for matrix with {len(matrix)} rows"
        )
    matrix.pop(position)
    return matrix


def search_2d(matrix, value):
    """Return (row, col) of the first occurrence of `value`, or None if not found."""
    for r, row in enumerate(matrix):
        for c, item in enumerate(row):
            if item == value:
                return (r, c)
    return None


def rotate_90_clockwise(matrix):
    """Return a new matrix rotated 90 degrees clockwise.
    For an m x n matrix the result is n x m. zip(*matrix[::-1]) is the
    standard idiom: reverse the row order, then transpose."""
    if not matrix:
        return matrix
    return [list(row) for row in zip(*matrix[::-1])]


def print_matrix(matrix):
    print("Matrix:")
    if not matrix:
        print("  (empty)")
        return
    for row in matrix:
        print(" ", row)


def read_row(expected_length=None):
    hint = f" ({expected_length} values)" if expected_length else ""
    raw = input(f"Enter row values space-separated{hint}: ")
    values = [int(x) for x in raw.split()]
    if expected_length is not None and len(values) != expected_length:
        raise ValueError(f"Expected {expected_length} values, got {len(values)}")
    return values


def menu():
    matrix = []
    print_matrix(matrix)

    actions = {
        "1": "Insert Row",
        "2": "Delete Row",
        "3": "Search Value",
        "4": "Rotate 90 Clockwise",
        "5": "Print Matrix",
        "6": "Exit",
    }

    while True:
        print("\n--- 2D Array Operations ---")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an operation: ").strip()

        try:
            if choice == "1":
                position = int(input("Position to insert row at: "))
                row = read_row(len(matrix[0]) if matrix else None)
                insert_row(matrix, position, row)
                print_matrix(matrix)

            elif choice == "2":
                position = int(input("Position of row to delete: "))
                delete_row(matrix, position)
                print_matrix(matrix)

            elif choice == "3":
                value = int(input("Value to search for: "))
                result = search_2d(matrix, value)
                if result is None:
                    print(f"{value} not found in the matrix")
                else:
                    print(f"{value} found at row {result[0]}, column {result[1]}")

            elif choice == "4":
                matrix = rotate_90_clockwise(matrix)
                print_matrix(matrix)

            elif choice == "5":
                print_matrix(matrix)

            elif choice == "6":
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