Section A: Concept Check — Answers
In Python, a 1D array is commonly implemented using a list.

Inserting an element at the beginning of a list requires shifting all (n) elements, making it an O(n) operation.

Deleting an element from the middle of a list requires shifting all elements after (to the right of) it, to fill the gap.

A left rotation by k positions moves the first k elements to the end of the array.

Linear search checks elements one by one, sequentially from the start while binary search requires the array to be sorted first.

A sparse matrix stores only non-zero elements, along with their row index and column index.

The standard triple format for a sparse matrix entry is (row, column, value).

Section B: Trace the Logic — Answers
1. Array operations on [10, 20, 30, 40, 50]
Step 1 — Insert 25 at index 2:

[10, 20, 25, 30, 40, 50]
(25 is placed at index 2; 30, 40, 50 each shift one position right)

Step 2 — Delete the element at index 0:

[20, 25, 30, 40, 50]
(10 is removed; every remaining element shifts one position left)

Step 3 — Rotate the resulting array left by 2 positions:

[30, 40, 50, 20, 25]
(the first 2 elements, 20 and 25, are moved to the end, in order)

2. Linear search for 19 in [5, 12, 8, 19, 3, 27]
Step	Index checked	Value at index	Match?
1	0	5	No
2	1	12	No
3	2	8	No
4	3	19	Yes — found at index 3
Search stops at step 4; the value is found at index 3.

3. Binary search for 15 in [2, 4, 7, 10, 15, 20, 22] (indices 0–6)
Step	low	high	mid	array[mid]	Comparison	Action
1	0	6	3	10	10 < 15	search right half → low = mid + 1 = 4
2	4	6	5	20	20 > 15	search left half → high = mid - 1 = 4
3	4	4	4	15	15 == 15	found at index 4
Value 15 is found at index 4 after 3 comparisons.

4. Sparse triple representation of D (row-major order)
D = [[0, 0, 5],
     [0, 8, 0],
     [3, 0, 0],
     [0, 0, 0]]
Scanning row by row, the non-zero entries are:

Row	Column	Value
0	2	5
1	1	8
2	0	3
Sparse triples: (0, 2, 5), (1, 1, 8), (2, 0, 3)

(Some conventions also prepend a header triple (4, 3, 3) meaning 4 rows, 3 columns, 3 non-zero entries — that header is counted separately from the data triples, per the note in Section D Q1.)

5. Storage comparison for matrix D
Full 2D representation: 4 rows × 3 columns = 12 values stored (every cell, zero or not).
Sparse representation: 3 non-zero entries × 3 values each (row, column, value) = 9 values stored (not counting the header).
For this particular small, fairly dense matrix (3 out of 12 entries non-zero, 25%), the sparse form still stores fewer raw values (9 vs 12) — but the gap is small, which is exactly the kind of data point Section D Q3 asks you to reason about at larger sizes and different densities.
