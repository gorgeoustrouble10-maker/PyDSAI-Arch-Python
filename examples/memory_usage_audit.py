"""Memory usage audit for PyDSAI data structures.

PyDSAI データ構造のメモリ使用量監査。
Measures physical memory (object graph size in Bytes) for ArrayList,
LinkedList, and BST at 10,000 and 50,000 elements.
Verifies __slots__ memory savings for Node classes.
"""

from __future__ import annotations

import gc
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any, Callable, Set

# Add src to path for pydsai import / pydsai インポート用に src をパスに追加
_SCRIPT_DIR = Path(__file__).resolve().parent
project_root = _SCRIPT_DIR.parent
sys.path.insert(0, str(project_root / "src"))

from pydsai import ArrayList, BinarySearchTree, DoublyLinkedList

# Audit configuration / 監査設定
SIZES = [10_000, 50_000]


def _deep_sizeof(obj: Any) -> int:
    """Iteratively compute total memory (Bytes) of object graph.

    オブジェクトグラフの総メモリ（バイト）を反復的に計算。
    Uses stack to avoid recursion limit. スタックで再帰制限を回避。

    Args:
        obj: Object to measure. 測定対象オブジェクト。

    Returns:
        Total size in bytes. 総サイズ（バイト）。
    """
    seen: Set[int] = set()
    stack: list[Any] = [obj]
    total = 0

    while stack:
        o = stack.pop()
        oid = id(o)
        if oid in seen:
            continue
        seen.add(oid)
        try:
            total += sys.getsizeof(o)
        except TypeError:
            continue

        if isinstance(o, (list, tuple)):
            for item in o:
                if item is not None:
                    stack.append(item)
        elif hasattr(o, "__dict__"):
            for v in o.__dict__.values():
                if v is not None:
                    stack.append(v)
        elif hasattr(o, "__slots__"):
            for slot in o.__slots__:
                if hasattr(o, slot):
                    val = getattr(o, slot)
                    if val is not None:
                        stack.append(val)

    return total


def _measure_structure(name: str, factory: Callable[[int], Any], n: int) -> int:
    """Create structure with n elements and return memory in Bytes.

    n 要素で構造を作成し、メモリ（バイト）を返す。

    Args:
        name: Structure name (for logging). 構造名（ログ用）。
        factory: Callable that creates and populates structure.
                 構造を作成・要素追加する呼び出し可能オブジェクト。
        n: Number of elements. 要素数。

    Returns:
        Memory in Bytes. メモリ（バイト）。
    """
    gc.collect()
    with redirect_stdout(io.StringIO()):
        structure = factory(n)
    size = _deep_sizeof(structure)
    return size


def run_audit() -> dict[str, dict[int, int]]:
    """Run memory audit for all structures at configured sizes.

    設定サイズで全構造のメモリ監査を実行。

    Returns:
        Dict[structure_name, Dict[size, bytes]].
    """
    results: dict[str, dict[int, int]] = {}

    def make_array_list(n: int) -> ArrayList:
        arr = ArrayList()
        for i in range(n):
            arr.add(i)
        return arr

    def make_linked_list(n: int) -> DoublyLinkedList:
        dll = DoublyLinkedList()
        for i in range(n):
            dll.add_last(i)
        return dll

    def make_bst(n: int) -> BinarySearchTree:
        bst = BinarySearchTree()
        for i in range(n):
            bst.insert(i)
        return bst

    results["ArrayList"] = {
        s: _measure_structure("ArrayList", make_array_list, s) for s in SIZES
    }
    results["DoublyLinkedList"] = {
        s: _measure_structure("DoublyLinkedList", make_linked_list, s) for s in SIZES
    }
    results["BinarySearchTree"] = {
        s: _measure_structure("BinarySearchTree", make_bst, s) for s in SIZES
    }

    return results


def _measure_slots_vs_dict(n: int = 10_000) -> tuple[int, int]:
    """Compare memory: N nodes with __slots__ vs with __dict__.

    __slots__ ありと __dict__ のみの N ノードのメモリを比較。

    Returns:
        (bytes_with_slots, bytes_with_dict).
    """

    class NodeWithSlots:
        __slots__ = ("value", "prev", "next")

        def __init__(self, v: Any, p: Any = None, n: Any = None) -> None:
            self.value = v
            self.prev = p
            self.next = n

    class NodeWithDict:
        def __init__(self, v: Any, p: Any = None, n: Any = None) -> None:
            self.value = v
            self.prev = p
            self.next = n

    gc.collect()
    with redirect_stdout(io.StringIO()):
        chain_slots: list[NodeWithSlots] = []
        prev: Any = None
        for i in range(n):
            node = NodeWithSlots(i, prev, None)
            if prev is not None:
                prev.next = node
            chain_slots.append(node)
            prev = node
    size_slots = _deep_sizeof(chain_slots)

    gc.collect()
    with redirect_stdout(io.StringIO()):
        chain_dict: list[NodeWithDict] = []
        prev = None
        for i in range(n):
            node = NodeWithDict(i, prev, None)
            if prev is not None:
                prev.next = node
            chain_dict.append(node)
            prev = node
    size_dict = _deep_sizeof(chain_dict)

    return size_slots, size_dict


def main() -> None:
    """Run audit, print table, and append results to docs/BENCHMARK_RESULTS.md.

    監査を実行し、表を表示、結果を docs/BENCHMARK_RESULTS.md に追記する。
    """
    print("PyDSAI Memory Usage Audit")
    print("=" * 60)
    print(f"Element counts: {SIZES}")
    print()

    # __slots__ vs __dict__ comparison / __slots__ と __dict__ の比較
    print("__slots__ vs __dict__ (10,000 linked nodes):")
    size_slots, size_dict = _measure_slots_vs_dict(10_000)
    saved = size_dict - size_slots
    pct = 100 * saved / size_dict if size_dict else 0
    print(f"  With __slots__:  {size_slots:>10,} B")
    print(f"  With __dict__:   {size_dict:>10,} B")
    print(f"  Saved:           {saved:>10,} B ({pct:.1f}%)")
    print()

    results = run_audit()

    # Print table / テーブル表示
    print(f"{'Structure':<20} | {'10,000 (B)':<12} | {'50,000 (B)':<12}")
    print("-" * 50)
    for name, sizes in results.items():
        print(f"{name:<20} | {sizes[10_000]:>10,} | {sizes[50_000]:>10,}")
    print()

    # Append to BENCHMARK_RESULTS.md / 結果を追記
    doc_path = project_root / "docs" / "BENCHMARK_RESULTS.md"
    doc_path.parent.mkdir(parents=True, exist_ok=True)

    header = "\n## Memory Usage Audit (Bytes)\n\nメモリ使用量監査（バイト）\n\n"
    table = (
        "| Structure | 10,000 elements | 50,000 elements |\n"
        "|-----------|-----------------|------------------|\n"
        f"| ArrayList | {results['ArrayList'][10_000]:,} | {results['ArrayList'][50_000]:,} |\n"
        f"| DoublyLinkedList | {results['DoublyLinkedList'][10_000]:,} | {results['DoublyLinkedList'][50_000]:,} |\n"
        f"| BinarySearchTree | {results['BinarySearchTree'][10_000]:,} | {results['BinarySearchTree'][50_000]:,} |\n"
    )

    if doc_path.exists():
        with open(doc_path, "a", encoding="utf-8") as f:
            f.write(header + table + "\n")
    else:
        with open(doc_path, "w", encoding="utf-8") as f:
            f.write("# PyDSAI Benchmark Results\n\nPyDSAI ベンチマーク結果\n\n")
            f.write(header + table + "\n")

    print(f"Results appended to: {doc_path}")


if __name__ == "__main__":
    main()
