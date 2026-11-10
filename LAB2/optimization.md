Section D: Space Optimization Analysis — Answers
(Based on running sparse_matrix.py / Program 3)

1. Space used, in terms of m, n, k
For an m x n matrix with k non-zero elements:

Full 2D representation: stores m x n values (every cell, zero or not).
Sparse triple representation: stores 3k values (k triples, 3 values per triple — row, column, value — not counting the header).
2. Test results
Two 6x6 matrices were run through Program 3's convert-to-sparse operation.

Sparse test matrix (roughly 80% zero):

0 0 0 2 0 0
0 5 0 0 0 0
0 0 0 0 8 0
0 0 0 0 8 0
0 0 0 6 0 0
0 0 9 0 0 4
Dense test matrix (fewer than 20% zero):

1 2 3 4 5 6
7 8 9 1 2 3
4 5 6 7 8 9
1 2 3 0 5 6
7 8 0 1 2 3
4 0 6 7 0 9
Matrix	Size	Zero elements	Non-zero (k)	Full stores (m×n)	Sparse stores (3k)
Sparse test	6x6 = 36	29 (80.6%)	7	36	21
Dense test	6x6 = 36	4 (11.1%)	32	36	96
Both were verified by reconstructing the full matrix from its sparse form with from_sparse — in both cases the reconstruction matched the original exactly.

3. Crossover point
The sparse representation only saves space while 3k < m x n, i.e. while:

k < (m x n) / 3
In other words, sparse storage stops saving space once more than roughly one-third (about 33%) of the elements are non-zero. Below that point, each non-zero element "costs" 3 stored values instead of 1, but you skip storing the (far more numerous) zeros; above that point, the 3x overhead per non-zero element outweighs the savings from skipping zeros.

The test data confirms this directly:

Sparse test matrix: 7/36 ≈ 19% non-zero (well under ⅓) → sparse wins, 21 vs 36
Dense test matrix: 32/36 ≈ 89% non-zero (well over ⅓) → sparse loses badly, 96 vs 36
4. Real-world example of a naturally sparse matrix
A large social network's adjacency matrix (rows and columns are users, entry = 1 if two users are connected) is naturally sparse: any individual user is directly connected to only a tiny fraction of the total user base, so the vast majority of entries in the full matrix are 0. Storing it as triples (or an equivalent adjacency-list structure) instead of a full grid is what makes it feasible to hold networks with millions of users in memory at all.

