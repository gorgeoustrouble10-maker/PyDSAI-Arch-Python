# Time and Space Complexity Reference

時間・空間計算量リファレンス

This document provides a comprehensive comparison of the core data structures in PyDSAI.

本ドキュメントは PyDSAI の主要データ構造の包括的な比較を提供します。

---

## Complexity Comparison Table

計算量比較表

| Data Structure | Operation | Time Complexity | Space Complexity |
|----------------|-----------|-----------------|------------------|
| **ArrayList** | Access by index (get) | O(1) | O(n) |
| | Insert at head | O(n)* | O(n) |
| | Insert at tail (add) | O(1) amortized | O(n) |
| | Delete at head | O(n)* | O(n) |
| | Delete at tail | O(1) | O(n) |
| | Search (by value) | O(n) | O(n) |
| **DoublyLinkedList** | Access by index (get) | O(n) | O(n) |
| | Insert at head | O(1) | O(n) |
| | Insert at tail | O(1) | O(n) |
| | Delete at head | O(1) | O(n) |
| | Delete at tail | O(1) | O(n) |
| | Search (by value) | O(n) | O(n) |
| **Stack** | Push (top) | O(1) amortized | O(n) |
| | Pop (top) | O(1) | O(n) |
| | Peek (top) | O(1) | O(n) |
| | Access by index | O(1) | O(n) |
| | Search | O(n) | O(n) |
| **Deque** | Add first | O(1) | O(n) |
| | Add last | O(1) | O(n) |
| | Remove first | O(1) | O(n) |
| | Remove last | O(1) | O(n) |
| | Peek first/last | O(1) | O(n) |
| | Access by index | O(n) | O(n) |
| | Search | O(n) | O(n) |
| **BinarySearchTree** | Insert | O(log n) avg, O(n) worst | O(n) |
| | Search | O(log n) avg, O(n) worst | O(n) |
| | Delete | O(log n) avg, O(n) worst | O(n) |
| | Inorder traversal | O(n) | O(n) |
| | get_min / get_max | O(log n) avg, O(n) worst | O(n) |

\* ArrayList does not natively support O(1) head insert/delete; shifting is required.

\* ArrayList は先頭への挿入・削除をネイティブにサポートせず、要素のシフトが必要。

---

## Deep Dive: Why ArrayList is Faster than LinkedList for Sequential Access

ディープダイブ：なぜ ArrayList は逐次アクセスで LinkedList より高速か

### Summary

Despite both having O(n) for a full sequential scan, **ArrayList significantly outperforms LinkedList** in practice. The root cause is **CPU cache behavior** and **spatial locality**.

両方とも逐次走査は O(n) だが、**ArrayList は実際に LinkedList より大幅に高速**である。根本原因は **CPU キャッシュの振る舞い**と**空間的局所性**である。

### Spatial Locality (空間的局所性)

**ArrayList:**
- Elements are stored in **contiguous memory** (連続メモリ).
- When the CPU loads element at index `i`, the cache fetches a **cache line** (typically 64 bytes) containing `i` and neighboring elements.
- Accessing `i+1`, `i+2`, ... often hits the **same cache line** — no additional memory reads.
- Result: **High cache hit rate**, minimal memory bandwidth usage.

**LinkedList:**
- Elements (nodes) are stored in **non-contiguous memory** (非連続メモリ); each node points to the next via a pointer.
- Traversing from node to node causes **random memory accesses**.
- Each node fetch may **evict** previously cached data (cache pollution).
- Result: **Low cache hit rate**, high memory bandwidth consumption, frequent **cache misses**.

### CPU Cache Concepts (CPU キャッシュの概念)

1. **Cache Line** (キャッシュライン): A fixed-size block (e.g., 64 bytes) transferred between main memory and cache. Accessing one byte loads the entire line.
2. **Cache Miss** (キャッシュミス): When requested data is not in cache — CPU stalls while fetching from RAM (100–300 cycles).
3. **Spatial Locality** (空間的局所性): If address X is accessed, addresses near X are likely to be accessed soon.
4. **Temporal Locality** (時間的局所性): If address X is accessed, X is likely to be accessed again soon.

ArrayList exploits **spatial locality**: adjacent elements share cache lines. LinkedList does not — each node can be anywhere in memory.

ArrayList は**空間的局所性**を活かす。LinkedList は活かせない。

### Empirical Impact (実測上の影響)

For iterating over 1 million integers:
- **ArrayList**: ~1–2 ms (cache-friendly).
- **LinkedList**: ~10–50 ms (cache-thrashing).

約 100 万整数の走査では、ArrayList は数 ms、LinkedList は数十 ms 程度になることが多い。

### When to Use Which (使い分け)

| Use ArrayList / 使用場面 | Use LinkedList / 使用場面 |
|-------------------------|---------------------------|
| Random access by index | Frequent head/tail insert/delete only |
| Sequential iteration | Queue/Deque with no index access |
| Cache-friendly workloads | Very large elements (pointer overhead less dominant) |

---

## Deep Dive: Binary Search Tree (BST)

ディープダイブ：二分探索木

### Core Properties (基本性質)

- **Left subtree** of a node contains only values **<** node.val.
- **Right subtree** of a node contains only values **>=** node.val.
- Both subtrees are also BSTs (recursive definition).
- **Inorder traversal** yields values in **sorted ascending order**.

### Time Complexity (時間計算量)

| Scenario | Insert | Search | Delete |
|----------|--------|--------|--------|
| **Best** (balanced) | O(log n) | O(log n) | O(log n) |
| **Average** (random insert order) | O(log n) | O(log n) | O(log n) |
| **Worst** (degenerate to linked list) | O(n) | O(n) | O(n) |

Worst case occurs when insertions are in ascending or descending order (e.g., 1, 2, 3, 4, 5), forming a linear chain.

最悪ケースは昇順・降順での挿入時に発生する。

### Applicable Scenarios (適用場面)

- Dynamic ordered set with frequent insert/search/delete.
- Range queries (with additional augmentation).
- Priority queue alternative (get_min/get_max in O(log n)).

### Advantages and Limitations (利点と制限)

| Advantages | Limitations |
|------------|-------------|
| O(log n) average for insert/search/delete | O(n) worst case (no balancing) |
| Inorder traversal yields sorted output | Hibbard deletion causes tree imbalance over time |
| Simpler than AVL/Red-Black | Not suitable for real-time or guaranteed latency |

**Degradation problem (劣化問題)**: Plain BST with Hibbard deletion (inorder successor replacement) tends to produce trees with height ~√n after many random deletions. Consider AVL or Red-Black trees for guaranteed O(log n) operations.

---

## BST Degeneration & Balancing

BST の劣化と平衡

### Why Monitor Balance Factor? (平衡係数を監視する理由)

The **balance factor** of a node is defined as:

ノードの**平衡係数**は次で定義される：

```
BF(node) = height(left subtree) - height(right subtree)
```

When **|BF| > 1**, the tree is **unbalanced**. Operations that should be O(log n) degrade toward O(n) because the worst path lengthens.

**|BF| > 1** のとき、木は**不平衡**である。本来 O(log n) である操作が、最悪経路の伸長により O(n) に近づく。

### Degeneration Scenarios (劣化シナリオ)

1. **Ascending/descending insert**: Inserting 1, 2, 3, 4, 5 in order produces a linked list. Height = n - 1.
2. **Hibbard deletion bias**: Repeated random deletions tend to skew the tree; height approaches √n.
3. **No rebalancing**: Plain BST never rotates; once unbalanced, it stays unbalanced.

### Use `get_balance_factor()` (get_balance_factor() の使い方)

PyDSAI's `BinarySearchTree` provides `get_balance_factor()` (root's BF) and `get_height()`. Use them to:

1. **Detect imbalance** before critical operations.
2. **Log metrics** for production monitoring.
3. **Decide when to rebuild** or migrate to AVL/Red-Black.

```python
bf = bst.get_balance_factor()
if abs(bf) > 1:
    # Consider rebalancing or switching to AVL
    pass
```

### Path to Self-Balancing (自己平衡への道)

| Structure | Balance guarantee | When to use |
|-----------|-------------------|-------------|
| Plain BST | None | Prototyping, small datasets |
| AVL Tree | |BF| ≤ 1 | Read-heavy, strict O(log n) |
| Red-Black | Height ≤ 2·log₂(n+1) | Insert/delete mix |

---

## Performance Real-world Test

実世界パフォーマンステスト

PyDSAI のベンチマークスイート（`examples/performance_benchmark.py`）による実測結果。  
実行: `python examples/performance_benchmark.py`  
結果は `benchmark_report.txt` に保存される。

| Benchmark | O(n) Structure | O(log n) / O(1) Structure | Time (ms) |
|-----------|----------------|---------------------------|-----------|
| **Search** (20K items, 100 iters) | ArrayList.search O(n) | BST.search O(log n) | 59.23 vs 70.67 |
| **Insert at head** (20K ops) | ArrayList.insert_at(0) O(n) | Deque.add_first O(1) | 10,284.56 vs 19.05 |
| **Full iteration** (20K items) | ArrayList (lock per get) | LinkedList (snapshot iter) | 28.33 vs 1.88 |

**Key takeaway**: Insert-at-head で **O(n) vs O(1)** の差が顕著（**約 540 倍**）。先頭挿入が頻繁な場合は Deque を選択すべき。

**重要な知見**：先頭挿入が頻繁な場合は Deque の採用で劇的な性能改善が期待できる。環境により変動あり。

---

## References

- [Cache-friendly code (Wikipedia)](https://en.wikipedia.org/wiki/Locality_of_reference)
- [Why Linked Lists are Slow (Bjarne Stroustrup)](https://isocpp.org/blog/2014/06/stroustrup-lists)
