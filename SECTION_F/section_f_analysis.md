# Section F: In-Depth Empirical & Theoretical Analysis

This document contains the answers and technical explanations for the six analytical questions in **Section F** of DAA Lab Task 3, connecting theoretical algorithm complexity with empirical measurements from the experiments conducted in Section D and Section E.

---

### Question 1: Performance on Already-Sorted Input vs Random Input

#### 1. Noticeably Worse on Already-Sorted Input:
* **Algorithm:** **Quick Sort (with last-element pivot)**.
* **Empirical Timing Comparison ($N = 2000$):**
  * Random Input: **$4.40$ ms** ($0.0044$ s)
  * Already-Sorted Input: **$330.58$ ms** ($0.3306$ s)
  * **Degradation:** Over **75x slowdown**!
* **Technical Explanation:**  
  In our implementation, the last element is selected as the pivot (`pivot = arr[high]`). When the input array is already sorted in ascending order, the element at index `high` is unconditionally the maximal element in the current subarray.  
  Consequently, the Lomuto partitioning subroutine places all other $n-1$ elements into the left subproblem and $0$ elements into the right subproblem. The recurrence relation degrades to:
  $$T(n) = T(n - 1) + T(0) + \Theta(n) = \Theta(n^2)$$
  The recursive call stack deepens to $O(n)$, performing $\sum_{i=1}^n i = \frac{n(n-1)}{2}$ comparisons instead of the balanced $O(n \log n)$ partitions achieved with randomized data.

#### 2. Algorithms that Stayed Roughly the Same:
* **Algorithms:** **Selection Sort, Merge Sort, and Heap Sort**.
* **Empirical Results ($N = 2000$):**
  * **Selection Sort:** $170.7$ ms (Random) vs $145.9$ ms (Sorted)
  * **Merge Sort:** $6.6$ ms (Random) vs $5.7$ ms (Sorted)
  * **Heap Sort:** $13.1$ ms (Random) vs $10.9$ ms (Sorted)
* **Technical Explanation:**
  * **Selection Sort:** The algorithm has an invariant loop structure. In every pass $i$, it exhaustively scans all remaining indices from $i+1$ to $n-1$ to locate the index of the minimum element. It performs exactly $\frac{n(n-1)}{2}$ comparisons in all cases, rendering it completely oblivious to the initial ordering.
  * **Merge Sort:** The divide step partitions the list strictly at index $\lfloor n / 2 \rfloor$ based on indices rather than element values. The recursion tree is strictly balanced with height $\lceil \log_2 n \rceil$, and merging two sorted halves of total length $n$ always requires between $n/2$ and $n-1$ comparisons. Thus, its time complexity is strictly $\Theta(n \log n)$ across all distributions.
  * **Heap Sort:** The algorithm first constructs a max-heap in $O(n)$ time and then performs $n$ extraction cycles, each involving swapping the root with the end element and performing an $O(\log n)$ `heapify` (sift-down) operation. Even if the array is already sorted, the heap construction and root-extraction operations must still restructure the complete binary tree, preserving its $O(n \log n)$ operational bound.

#### 3. Noticeably Faster on Already-Sorted Input:
* **Algorithms:** **Bubble Sort and Insertion Sort**.
  * **Bubble Sort:** Dropped from $364.8$ ms (Random) to **$0.30$ ms** (Sorted) at $N=2000$. The pass flag detected zero swaps during Pass 1, triggering an immediate early exit in $\Theta(n)$ time.
  * **Insertion Sort:** Dropped from $177.0$ ms (Random) to **$0.40$ ms** (Sorted) at $N=2000$. The while-loop condition `arr[j] > key` evaluated to `False` on the very first comparison for every element, reducing comparisons to $n-1$ ($\Theta(n)$ best case).

---

### Question 2: Bubble Sort vs Selection Sort vs Insertion Sort on Reverse-Sorted Input

#### Empirical Results ($N = 2000$, Reverse-Sorted):
* **Selection Sort:** **$166.86$ ms** (Fastest)
* **Insertion Sort:** **$324.00$ ms** (Middle)
* **Bubble Sort:** **$464.99$ ms** (Slowest)

#### Complexity Analysis and Justification:
Yes, this empirical ordering strictly matches theoretical expectations despite all three algorithms having a theoretical worst-case time complexity of $O(n^2)$. The divergence is governed by **constant factors and the cost of memory writes / swaps**:

1. **Selection Sort is Fastest:**  
   Selection Sort performs $\frac{n(n-1)}{2}$ comparisons, but it only performs at most **$n - 1$ swaps** across the entire algorithm execution. In Python, comparing two integers in a loop has low overhead compared to mutating lists.
2. **Insertion Sort is in the Middle:**  
   On reverse-sorted data, every new element is strictly smaller than all elements in the sorted prefix. It must be compared against all $i$ previous elements and shifted one position right. This results in $\frac{n(n-1)}{2}$ comparisons and $\frac{n(n-1)}{2}$ single-variable shift assignments (`arr[j+1] = arr[j]`).
3. **Bubble Sort is Slowest:**  
   Every single adjacent comparison in reverse-sorted data is inverted ($arr[j] > arr[j+1]$). Bubble Sort performs $\frac{n(n-1)}{2}$ comparisons **and** $\frac{n(n-1)}{2}$ full pairwise swaps. In Python, a tuple swap (`arr[j], arr[j+1] = arr[j+1], arr[j]`) involves bytecode instructions for tuple packing, unpacking, and two separate write operations per inversion, creating immense operational overhead.

---

### Question 3: Divide-and-Conquer Difference: Merge Sort vs Quick Sort

#### Architectural Comparison:
Both Merge Sort and Quick Sort are divide-and-conquer algorithms, but their division principles differ fundamentally:
* **Merge Sort (Value-Agnostic Division):**  
  Splits the array at the geometric midpoint $mid = \lfloor (low + high) / 2 \rfloor$. The division is independent of the keys, always producing two halves of size $\approx n/2$. The recurrence:
  $$T(n) = 2T(n/2) + O(n) = \Theta(n \log n)$$
  holds universally across sorted, reverse-sorted, and random arrays.

* **Quick Sort (Data-Driven Partitioning & Pivot Strategy):**  
  Quick Sort's partition point depends strictly on the value of the chosen pivot relative to the other keys.  
  * **Our Pivot Strategy:** We chose the **last element** of the subarray (`pivot = arr[high]`).
  * **Impact on Already-Sorted Input:**  
    Because every subarray `arr[low..high]` is already in ascending order, the last element `arr[high]` is guaranteed to be the **absolute maximum value** in that range.
  * **Resulting Partition:**  
    All $n - 1$ other elements are strictly less than or equal to the pivot, placing the pivot at index $high$ and resulting in two subproblems of size $n - 1$ and $0$.
  * **Degenerate Tree:**  
    The recursion tree becomes a skewed unary chain of depth $n$ rather than a balanced binary tree of depth $\log_2 n$. This yields $\sum_{k=1}^n k = \frac{n(n+1)}{2} = \Theta(n^2)$ comparisons, causing the observed 75x slowdown.

---

### Question 4: Radix Sort Performance and Practical Limitations

#### Performance Relative to Comparison Sorts:
Radix Sort operates in non-comparison linear time:
$$O(d \cdot (n + k))$$
where $d$ is the number of digits in the maximum element, $n$ is array length, and $k$ is the radix base ($k=10$ for decimal digits).  
Because it does not compare keys, it is not bound by the $\Omega(n \log n)$ theoretical lower bound of comparison-based sorting. For moderate numbers of digits (e.g., $d \le 4$), Radix Sort executes in linear time $O(n)$, rivaling or outperforming Quick Sort and Merge Sort.

#### Factors Limiting Its Usefulness:
1. **Non-Integer or Complex Data Types:**  
   Radix Sort relies on dissecting keys into discrete positional digits or characters. Supporting floating-point numbers (IEEE 754 signs, exponents, mantissas), negative integers, variable-length unicode strings, or complex domain objects requires elaborate transformation and normalization routines.
2. **Massive Value Ranges (Large $d$):**  
   If an array has small size $n = 100$ but contains 64-bit integers up to $10^{18}$, the number of decimal passes is $d = 18$. The total operations are $18 \times (100 + 10) = 1980$, which is noticeably slower than a comparison sort's $100 \log_2(100) \approx 664$ operations. When $d = \Omega(n)$, Radix Sort degrades to quadratic complexity.
3. **Memory Overhead:**  
   LSD Radix Sort is not an in-place algorithm; each digit pass requires an auxiliary output array of size $n$ and bucket arrays of size $k$. For memory-constrained environments, in-place algorithms like Heap Sort or Quick Sort are strongly preferred.

---

### Question 5: Search Step Comparisons in Search Engine Simulator

#### Empirical Comparison ($N = 35$ Vocabulary Words):
| Query Tested | Target Status | Binary Search Comparisons | Hash Table (Chaining) Comparisons | Hash Table (Linear Probing) Probes |
| :--- | :---: | :---: | :---: | :---: |
| `"algorithm"` | Present | 5 steps | **1 step** | **1 step** |
| `"recursion"` | Present | 3 steps | **1 step** | **1 step** |
| `"zero"` | Present | 6 steps | **2 steps** | **3 steps** |
| `"hashing"` | Absent | 5 steps | **1 step** | **4 steps** |
| `"quantum"` | Absent | 5 steps | **1 step** | **2 steps** |

#### Theoretical Alignment:
* **Fewest Steps:** The **Hash Tables** required the fewest steps (averaging 1.0 to 1.5 checks), while Binary Search consistently took 3 to 6 comparisons.
* **Match with Theoretical Complexity:**
  * **Binary Search:** Operates in $\Theta(\log_2 n)$ time. For $n=35$, $\lceil \log_2(35) \rceil = 6$ comparisons maximum, which matches our observed range of 3–6 steps.
  * **Hash Tables:** Achieve expected $O(1)$ constant time lookup. When using a prime table size with controlled load factor $\alpha$, computing $h(key)$ maps the search directly to the candidate bucket in 1 step, followed by 0 to 2 collision probes.

---

### Question 6: Separate Chaining vs Linear Probing & 90% Occupancy

#### 1. Performance on Lab Dataset:
For our specific 35-word dataset, **Separate Chaining** handled collisions better and more uniformly.
* Chaining table size was prime (47), giving load factor $\alpha = 35 / 47 \approx 0.74$. Most buckets held 0 or 1 item, and no chain exceeded 2 items. Unsuccessful searches in empty buckets terminated in 1 check.
* Linear probing table size was prime (53), giving load factor $\alpha = 35 / 53 \approx 0.66$. While average search was fast, mild primary clustering occurred (e.g., searching for missing word `"hashing"` required 4 probes before finding an empty slot).

#### 2. Behavior if Table Were 90% Full ($\alpha = 0.90$):
**Yes, the difference would change drastically in favor of Separate Chaining.**

* **Linear Probing Suffers from Severe Primary Clustering:**  
  In open addressing with linear probing, occupied slots tend to coalesce into contiguous blocks. As $\alpha \to 1.0$, the probability of hashing into an existing cluster increases, and each collision extends the cluster length.  
  The theoretical expected number of probes for an **unsuccessful search** in linear probing is:
  $$\mathbb{E}[\text{Probes}_{\text{unsuccessful}}] = \frac{1}{2} \left(1 + \frac{1}{(1 - \alpha)^2}\right)$$
  For $\alpha = 0.90$:
  $$\mathbb{E}[\text{Probes}_{\text{unsuccessful}}] = \frac{1}{2} \left(1 + \frac{1}{(0.10)^2}\right) = \frac{1}{2}(1 + 100) = \mathbf{50.5\text{ probes!}}$$
  For a **successful search**, the expected probes rise to:
  $$\mathbb{E}[\text{Probes}_{\text{successful}}] = \frac{1}{2} \left(1 + \frac{1}{1 - \alpha}\right) = \frac{1}{2}(1 + 10) = \mathbf{5.5\text{ probes}}$$

* **Separate Chaining Degrades Linearly and Gracefully:**  
  In separate chaining, keys in different buckets never interfere with one another; there is zero clustering across buckets.  
  For $\alpha = 0.90$:
  * Expected comparisons for successful search: $1 + \frac{\alpha}{2} = 1 + 0.45 = \mathbf{1.45\text{ comparisons}}$.
  * Expected comparisons for unsuccessful search: $\alpha = \mathbf{0.90\text{ comparisons}}$.

**Conclusion:** At high occupancies like 90%, Linear Probing deteriorates catastrophically ($50.5$ probes per miss), whereas Separate Chaining remains nearly optimal ($1.45$ comparisons).
