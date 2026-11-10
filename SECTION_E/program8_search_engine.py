"""
Program 8: Search Engine Simulator
Simplified search engine storing words mapped to document IDs and frequencies.
Implements and compares three lookup strategies:
1. Binary Search on a sorted word list
2. Hash Table with Separate Chaining (custom hash function)
3. Hash Table with Linear Probing (custom hash function)
Reports whether a word is found along with the number of comparisons/probes required by each.
"""

import sys

# Predefined dictionary of 35 computer science words mapped to document metadata
WORD_DATABASE = {
    "algorithm":   {"doc_id": "DOC_01", "frequency": 42},
    "array":       {"doc_id": "DOC_02", "frequency": 18},
    "binary":      {"doc_id": "DOC_03", "frequency": 27},
    "compiler":    {"doc_id": "DOC_04", "frequency": 12},
    "database":    {"doc_id": "DOC_05", "frequency": 35},
    "encryption":  {"doc_id": "DOC_06", "frequency": 14},
    "framework":   {"doc_id": "DOC_07", "frequency": 22},
    "function":    {"doc_id": "DOC_08", "frequency": 50},
    "graph":       {"doc_id": "DOC_09", "frequency": 31},
    "hash":        {"doc_id": "DOC_10", "frequency": 40},
    "indexing":    {"doc_id": "DOC_11", "frequency": 19},
    "json":        {"doc_id": "DOC_12", "frequency": 25},
    "kernel":      {"doc_id": "DOC_13", "frequency": 16},
    "latency":     {"doc_id": "DOC_14", "frequency": 11},
    "memory":      {"doc_id": "DOC_15", "frequency": 29},
    "network":     {"doc_id": "DOC_16", "frequency": 38},
    "object":      {"doc_id": "DOC_17", "frequency": 45},
    "operating":   {"doc_id": "DOC_18", "frequency": 15},
    "pipeline":    {"doc_id": "DOC_19", "frequency": 20},
    "pointer":     {"doc_id": "DOC_20", "frequency": 17},
    "queue":       {"doc_id": "DOC_21", "frequency": 23},
    "recursion":   {"doc_id": "DOC_22", "frequency": 28},
    "search":      {"doc_id": "DOC_23", "frequency": 60},
    "socket":      {"doc_id": "DOC_24", "frequency": 13},
    "sorting":     {"doc_id": "DOC_25", "frequency": 47},
    "stack":       {"doc_id": "DOC_26", "frequency": 26},
    "thread":      {"doc_id": "DOC_27", "frequency": 33},
    "tree":        {"doc_id": "DOC_28", "frequency": 37},
    "unicode":     {"doc_id": "DOC_29", "frequency": 10},
    "variable":    {"doc_id": "DOC_30", "frequency": 48},
    "virtual":     {"doc_id": "DOC_31", "frequency": 21},
    "web":         {"doc_id": "DOC_32", "frequency": 52},
    "x86":         {"doc_id": "DOC_33", "frequency": 8},
    "yaml":        {"doc_id": "DOC_34", "frequency": 9},
    "zero":        {"doc_id": "DOC_35", "frequency": 7},
}


def custom_hash(key_str, table_size):
    """
    Custom polynomial rolling hash function.
    h = sum(ord(char) * 31^i) % table_size
    Produces uniform distribution over table_size.
    """
    p = 31
    hash_val = 0
    for i, ch in enumerate(key_str):
        hash_val = (hash_val * p + ord(ch))
    return hash_val % table_size


# =====================================================================
# 1. Separate Chaining Hash Table
# =====================================================================
class HashTableChaining:
    def __init__(self, size=47):
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.count = 0

    def insert(self, key, value):
        idx = custom_hash(key, self.size)
        bucket = self.table[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.count += 1

    def search(self, key):
        """
        Returns: (found: bool, value: dict, comparisons: int)
        """
        idx = custom_hash(key, self.size)
        bucket = self.table[idx]
        comparisons = 0
        if not bucket:
            # Bucket is empty, 1 slot check confirmed absence
            return False, None, 1

        for k, v in bucket:
            comparisons += 1
            if k == key:
                return True, v, comparisons

        return False, None, comparisons


# =====================================================================
# 2. Linear Probing Hash Table
# =====================================================================
class HashTableLinearProbing:
    def __init__(self, size=53):
        # Using prime size > 35 to maintain load factor ~ 0.66
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def insert(self, key, value):
        idx = custom_hash(key, self.size)
        probes = 0
        while probes < self.size:
            curr_idx = (idx + probes) % self.size
            if self.table[curr_idx] is None:
                self.table[curr_idx] = (key, value)
                self.count += 1
                return
            elif self.table[curr_idx][0] == key:
                self.table[curr_idx] = (key, value)
                return
            probes += 1
        raise OverflowError("Hash table is full")

    def search(self, key):
        """
        Returns: (found: bool, value: dict, probes: int)
        """
        idx = custom_hash(key, self.size)
        probes = 0
        while probes < self.size:
            curr_idx = (idx + probes) % self.size
            probes += 1
            entry = self.table[curr_idx]
            if entry is None:
                return False, None, probes
            if entry[0] == key:
                return True, entry[1], probes
        return False, None, probes


# =====================================================================
# 3. Binary Search on Sorted Word List
# =====================================================================
def binary_search_lookup(sorted_list, target_word):
    """
    Returns: (found: bool, value: dict, comparisons: int)
    """
    low = 0
    high = len(sorted_list) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        mid_word, mid_val = sorted_list[mid]

        if mid_word == target_word:
            return True, mid_val, comparisons
        elif mid_word < target_word:
            low = mid + 1
        else:
            high = mid - 1

    return False, None, comparisons


# =====================================================================
# Unified Search Engine Interface
# =====================================================================
class SearchEngineSimulator:
    def __init__(self, dataset):
        self.dataset = dataset
        # 1. Sorted list for binary search
        self.sorted_words = sorted(dataset.items(), key=lambda x: x[0])
        # 2. Hash table with separate chaining
        self.chaining_table = HashTableChaining(size=47)
        # 3. Hash table with linear probing
        self.probing_table = HashTableLinearProbing(size=53)

        for word, meta in dataset.items():
            self.chaining_table.insert(word, meta)
            self.probing_table.insert(word, meta)

    def query(self, word):
        word = word.strip().lower()
        bs_found, bs_val, bs_steps = binary_search_lookup(self.sorted_words, word)
        sc_found, sc_val, sc_steps = self.chaining_table.search(word)
        lp_found, lp_val, lp_steps = self.probing_table.search(word)

        return {
            "word": word,
            "binary_search": {"found": bs_found, "val": bs_val, "steps": bs_steps},
            "chaining": {"found": sc_found, "val": sc_val, "steps": sc_steps},
            "probing": {"found": lp_found, "val": lp_val, "steps": lp_steps},
        }


def display_query_result(res):
    word = res["word"]
    print(f"\n=============================================================")
    print(f"SEARCH RESULTS FOR: '{word}'")
    print(f"=============================================================")
    print(f"{'Method':<25} | {'Found?':<8} | {'Steps (Comps/Probes)':>20} | {'Metadata'}")
    print("-" * 75)
    for method_name, key in [
        ("Binary Search", "binary_search"),
        ("Hash Table (Chaining)", "chaining"),
        ("Hash Table (Linear Probe)", "probing"),
    ]:
        m = res[key]
        found_str = "YES" if m["found"] else "NO"
        steps_str = f"{m['steps']} step(s)"
        meta_str = f"Doc: {m['val']['doc_id']}, Freq: {m['val']['frequency']}" if m["found"] else "N/A"
        print(f"{method_name:<25} | {found_str:<8} | {steps_str:>20} | {meta_str}")


def run_demo():
    print("=" * 70)
    print("       SEARCH ENGINE SIMULATOR - DEMONSTRATION MODE         ")
    print(f"Total vocabulary size: {len(WORD_DATABASE)} words")
    print("=" * 70)

    engine = SearchEngineSimulator(WORD_DATABASE)

    test_queries = [
        "algorithm",  # First in sorted database
        "recursion",  # Middle word
        "zero",       # Last word in sorted database
        "hashing",    # Not present (near 'hash')
        "quantum",    # Completely absent word
    ]

    for q in test_queries:
        res = engine.query(q)
        display_query_result(res)


def interactive_mode():
    engine = SearchEngineSimulator(WORD_DATABASE)
    print("=" * 60)
    print("SEARCH ENGINE SIMULATOR - INTERACTIVE SEARCH")
    print(f"Loaded {len(WORD_DATABASE)} words. Type 'exit' to quit.")
    print("=" * 60)
    while True:
        q = input("\nEnter search term: ").strip()
        if not q or q.lower() == "exit":
            print("Exiting search engine.")
            break
        res = engine.query(q)
        display_query_result(res)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        run_demo()