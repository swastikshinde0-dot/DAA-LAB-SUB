"""
Program 1: 1D Array Operations
Supports insert, delete, linear search, and left/right rotation
on a Python list acting as a 1D array.
"""


def insert_at_index(arr, index, value):
    """Insert `value` at `index`. Valid indices: 0 to len(arr) (inclusive)."""
    if index < 0 or index > len(arr):
        raise IndexError(f"Insert index {index} out of bounds for array of size {len(arr)}")
    arr.insert(index, value)
    return arr


def delete_at_index(arr, index):
    """Delete the element at `index`. Valid indices: 0 to len(arr) - 1."""
    if len(arr) == 0:
        raise IndexError("Cannot delete from an empty array")
    if index < 0 or index >= len(arr):
        raise IndexError(f"Delete index {index} out of bounds for array of size {len(arr)}")
    arr.pop(index)
    return arr


def linear_search(arr, value):
    """Return the index of the first occurrence of `value`, or -1 if not found."""
    for i, item in enumerate(arr):
        if item == value:
            return i
    return -1


def rotate_left(arr, k):
    """Return a new list rotated left by k positions."""
    n = len(arr)
    if n == 0:
        return arr[:]
    k = k % n  # normalize so k >= n behaves the same as k % n
    return arr[k:] + arr[:k]


def rotate_right(arr, k):
    """Return a new list rotated right by k positions."""
    n = len(arr)
    if n == 0:
        return arr[:]
    k = k % n
    if k == 0:
        return arr[:]
    return arr[-k:] + arr[:-k]


def print_array(arr):
    print("Array:", arr)


def menu():
    arr = []
    print_array(arr)

    actions = {
        "1": "Insert",
        "2": "Delete",
        "3": "Linear Search",
        "4": "Rotate Left",
        "5": "Rotate Right",
        "6": "Print Array",
        "7": "Exit",
    }

    while True:
        print("\n--- 1D Array Operations ---")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an operation: ").strip()

        try:
            if choice == "1":
                index = int(input("Index to insert at: "))
                value = int(input("Value to insert: "))
                insert_at_index(arr, index, value)
                print_array(arr)

            elif choice == "2":
                index = int(input("Index to delete: "))
                delete_at_index(arr, index)
                print_array(arr)

            elif choice == "3":
                value = int(input("Value to search for: "))
                result = linear_search(arr, value)
                if result == -1:
                    print(f"{value} not found in the array")
                else:
                    print(f"{value} found at index {result}")

            elif choice == "4":
                k = int(input("Rotate left by how many positions? "))
                arr = rotate_left(arr, k)
                print_array(arr)

            elif choice == "5":
                k = int(input("Rotate right by how many positions? "))
                arr = rotate_right(arr, k)
                print_array(arr)

            elif choice == "6":
                print_array(arr)

            elif choice == "7":
                print("Exiting.")
                break

            else:
                print("Invalid choice, try again.")

        except ValueError:
            print("Invalid input: please enter a valid integer.")
        except IndexError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu()