"""
Lab Task 2 - Part 2: Stack or Queue
Tasks arriving in order: Task1, Task2, Task3, Task4, Task5

1. Order completed if served using a Stack (LIFO)
2. Order completed if served using a Queue (FIFO)
3. Which structure should a printer use? Show the print order.
"""

from collections import deque

tasks = ["Task1", "Task2", "Task3", "Task4", "Task5"]


def run_as_stack(items):
    """LIFO: push everything, then pop -> reverse arrival order."""
    stack = []
    for t in items:
        stack.append(t)
        print(f"Push {t} -> stack: {stack}")

    order = []
    while stack:
        popped = stack.pop()
        order.append(popped)
        print(f"Pop {popped} -> stack: {stack}")
    return order


def run_as_queue(items):
    """FIFO: enqueue everything, then dequeue -> same as arrival order."""
    queue = deque()
    for t in items:
        queue.append(t)
        print(f"Enqueue {t} -> queue: {list(queue)}")

    order = []
    while queue:
        dequeued = queue.popleft()
        order.append(dequeued)
        print(f"Dequeue {dequeued} -> queue: {list(queue)}")
    return order


if __name__ == "__main__":
    print("Input:", tasks)

    print("\n--- Stack (LIFO) simulation ---")
    stack_order = run_as_stack(tasks)
    print(f"\nCompletion order using a Stack: {stack_order}")

    print("\n--- Queue (FIFO) simulation ---")
    queue_order = run_as_queue(tasks)
    print(f"\nCompletion order using a Queue: {queue_order}")

    print("\n--- Printer decision ---")
    print("A printer must serve jobs first-come-first-served, so it should use a QUEUE.")
    print(f"Print order (Task1 to Task5): {queue_order}")