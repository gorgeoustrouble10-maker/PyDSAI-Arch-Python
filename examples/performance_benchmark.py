"""Performance benchmark suite for PyDSAI data structures.

PyDSAI データ構造の性能ベンチマークスイート。
Compares ArrayList vs BST (search), ArrayList vs Deque (insert-at-head),
ArrayList vs LinkedList (full iteration).
"""

from __future__ import annotations

import io
import sys
import time
from contextlib import redirect_stdout
from pathlib import Path
from typing import Callable

# Add src to path for pydsai import / pydsai インポート用に src をパスに追加
_SCRIPT_DIR = Path(__file__).resolve().parent
project_root = _SCRIPT_DIR.parent
sys.path.insert(0, str(project_root / "src"))

from pydsai import ArrayList, BinarySearchTree, Deque, DoublyLinkedList

# Benchmark configuration / ベンチマーク設定
N_ITEMS = 20_000
N_SEARCH_ITERATIONS = 100  # Number of search ops to average / 検索回数の平均


def _time_ms(func: Callable[[], object]) -> float:
    """Run func and return elapsed milliseconds. Suppresses stdout (log_operation).

    func を実行し経過ミリ秒を返す。log_operation の出力を抑制。

    Args:
        func: Callable with no args. 引数なしの呼び出し可能オブジェクト。

    Returns:
        Elapsed time in milliseconds. 経過時間（ミリ秒）。
    """
    start = time.perf_counter()
    with redirect_stdout(io.StringIO()):
        func()
    return (time.perf_counter() - start) * 1000


def benchmark_search() -> tuple[float, float]:
    """Compare ArrayList O(n) linear search vs BST O(log n) search.

    ArrayList O(n) 線形検索と BST O(log n) 検索を比較。

    Returns:
        (arr_ms, bst_ms): Time in ms for each. 各々の所要時間（ミリ秒）。
    """
    with redirect_stdout(io.StringIO()):
        arr = ArrayList()
        bst = BinarySearchTree()
        for i in range(N_ITEMS):
            arr.add(i)
            bst.insert(i)

    target = (
        N_ITEMS - 1
    )  # Worst case for ArrayList (at end) / ArrayList 最悪ケース（末尾）

    def arr_search() -> None:
        for _ in range(N_SEARCH_ITERATIONS):
            arr.search(target)

    def bst_search() -> None:
        for _ in range(N_SEARCH_ITERATIONS):
            bst.search(target)

    arr_ms = _time_ms(arr_search)
    bst_ms = _time_ms(bst_search)
    return arr_ms, bst_ms


def benchmark_insert_at_head() -> tuple[float, float]:
    """Compare ArrayList.insert_at(0) O(n) vs Deque.add_first O(1).

    ArrayList.insert_at(0) O(n) と Deque.add_first O(1) を比較。

    Returns:
        (arr_ms, dq_ms): Time in ms for each. 各々の所要時間（ミリ秒）。
    """
    arr = ArrayList()
    dq = Deque()

    def arr_insert() -> None:
        for i in range(N_ITEMS):
            arr.insert_at(0, i)

    def dq_insert() -> None:
        for i in range(N_ITEMS):
            dq.add_first(i)

    arr_ms = _time_ms(arr_insert)
    dq_ms = _time_ms(dq_insert)
    return arr_ms, dq_ms


def benchmark_iteration() -> tuple[float, float]:
    """Compare ArrayList vs LinkedList full traversal (Spatial Locality impact).

    ArrayList と LinkedList の全走査を比較（空間的局所性の影響）。

    Returns:
        (arr_ms, dll_ms): Time in ms for each. 各々の所要時間（ミリ秒）。
    """
    with redirect_stdout(io.StringIO()):
        arr = ArrayList()
        dll = DoublyLinkedList()
        for i in range(N_ITEMS):
            arr.add(i)
            dll.add_last(i)

    def arr_iterate() -> object:
        total = 0
        for i in range(arr.size()):
            total += arr.get(i)
        return total

    def dll_iterate() -> object:
        total = 0
        for v in dll:
            total += v
        return total

    arr_ms = _time_ms(arr_iterate)
    dll_ms = _time_ms(dll_iterate)
    return arr_ms, dll_ms


def run_all() -> dict[str, tuple[float, float]]:
    """Run all benchmarks and return results as dict.

    全ベンチマークを実行し、結果を辞書で返す。

    Returns:
        Dict mapping benchmark name to (time_a, time_b). ベンチマーク名→(時間A, 時間B)。
    """
    return {
        "Search (20K items)": benchmark_search(),
        "Insert at head (20K ops)": benchmark_insert_at_head(),
        "Full iteration (20K items)": benchmark_iteration(),
    }


def main() -> None:
    """Run benchmarks, print results table, and save report to benchmark_report.txt.

    ベンチマークを実行し、結果表を表示、benchmark_report.txt に保存する。
    """
    print("PyDSAI Performance Benchmark")
    print("=" * 60)
    print(f"Config: N_ITEMS={N_ITEMS:,}, N_SEARCH_ITERATIONS={N_SEARCH_ITERATIONS}")
    print()

    results = run_all()

    # Table header / テーブルヘッダ
    print(f"{'Benchmark':<35} | {'Structure':<28} | {'Time (ms)':<12}")
    print("-" * 78)

    rows: list[str] = []
    for name, (a_ms, b_ms) in results.items():
        if "Search" in name:
            label_a, label_b = "ArrayList.search O(n)", "BST.search O(log n)"
        elif "Insert" in name:
            label_a, label_b = "ArrayList.insert_at(0) O(n)", "Deque.add_first O(1)"
        else:
            label_a, label_b = "ArrayList (lock per get)", "LinkedList (snapshot iter)"

        print(f"{name:<35} | {label_a:<28} | {a_ms:>10.2f}")
        print(f"{'':<35} | {label_b:<28} | {b_ms:>10.2f}")
        print("-" * 78)
        rows.append(f"{name}\n  {label_a}: {a_ms:.2f} ms\n  {label_b}: {b_ms:.2f} ms")

    # Save report / レポート保存
    report_path = project_root / "benchmark_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("PyDSAI Performance Benchmark Report\n")
        f.write("PyDSAI 性能ベンチマークレポート\n")
        f.write("=" * 50 + "\n")
        f.write(f"N_ITEMS={N_ITEMS}, N_SEARCH_ITERATIONS={N_SEARCH_ITERATIONS}\n\n")
        for row in rows:
            f.write(row + "\n\n")
    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
