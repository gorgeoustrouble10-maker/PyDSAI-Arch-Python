# PyDSAI — データ構造・アルゴリズムライブラリ

**Python Data Structures & Algorithms Implementation**

---

## ① プロジェクト概要（Project Overview）

PyDSAI は、AI 時代のデータ構造とアルゴリズムを体系的に実装した Python ライブラリである。**契約による設計（Design by Contract）**、**継承より合成（Composition over Inheritance）**、**スレッドセーフ**を徹底し、企業級の品質を担保している。

---

## ② 対応データ構造一覧

| データ構造 | 英語名 | 特徴 |
|-----------|--------|------|
| **動的配列** | ArrayList | 連続メモリ配置、O(1) インデックスアクセス、容量倍増による動的拡張、スレッドセーフ |
| **双方向連結リスト** | DoublyLinkedList | 先頭・末尾 O(1) 挿入・削除、head/tail ポインタ管理、スレッドセーフ |
| **二分探索木** | BinarySearchTree | O(log n) 検索・挿入・削除、中順走査で昇順取得、スレッドセーフ |
| **スタック** | Stack | LIFO（後入れ先出し）、ArrayList を内部ストアに合成、push/pop/peek 提供 |
| **デック（両端キュー）** | Deque | 両端 O(1) 操作、DoublyLinkedList を内部に合成、Queue モード（enqueue/dequeue）・Stack モード（push/pop）に対応 |

> **補足**：Queue（キュー）の FIFO 操作は、Deque の `enqueue` / `dequeue` により実現している。

---

## ③ 設計思想（Design Philosophy）

### 3.1 契約による設計（Design by Contract）

**実装背景**：`abc` モジュールにより `LinearList` 抽象基底クラスを定義し、`add`・`remove`・`get`・`size` の 4 メソッドを契約として明示している。ArrayList、DoublyLinkedList、Stack、Deque はすべて `LinearList` を継承し、同一インターフェースで利用可能である。

**メリット**：実装を差し替えても呼び出し側の変更が不要となり、拡張性とテスタビリティが向上する。依存性逆転の原則（DIP）に沿った設計である。

### 3.2 継承より合成（Composition over Inheritance）

**実装背景**：Stack は内部で ArrayList を、Deque は DoublyLinkedList を保持する「合成」により実装している。基底クラスの実装に縛られず、適切な内部データ構造を選択できる。

**メリット**：クラス階層を浅く保ちつつ、責務の分離と再利用性を高めている。GoF のデザインパターンにおける「合成による柔軟性」の実践である。

### 3.3 スレッドセーフ設計（Thread-Safe Design）

**実装背景**：ArrayList と DoublyLinkedList の基底層に `threading.Lock` を導入し、すべての読み書き操作を保護している。複数メソッドにまたがる操作（例：`pop_last`・`peek_last`）は、単一ロック内で完了する原子的操作として実装し、競合状態を排除している。

**メリット**：マルチスレッド環境でもデータの整合性が保たれ、デッドロックのリスクを抑える設計となっている。

---

## ④ 時間計算量・空間計算量

`docs/COMPLEXITY.md` の内容を基に、主要操作の計算量を抜粋する。

| データ構造 | 操作 | 時間計算量 | 空間計算量 |
|-----------|------|-----------|-----------|
| **ArrayList** | インデックスアクセス（get） | O(1) | O(n) |
| | 末尾挿入（add） | O(1) 償却 | O(n) |
| | 先頭挿入・削除 | O(n)* | O(n) |
| | 値による検索 | O(n) | O(n) |
| **DoublyLinkedList** | インデックスアクセス（get） | O(n) | O(n) |
| | 先頭・末尾挿入・削除 | O(1) | O(n) |
| | 値による検索 | O(n) | O(n) |
| **Stack** | push / pop / peek | O(1) | O(n) |
| **Deque** | add_first / add_last / remove_first / remove_last / peek | O(1) | O(n) |
| | インデックスアクセス（get） | O(n) | O(n) |

\* ArrayList の先頭操作は、要素シフトのため O(n)。

---

## ⑤ 環境要件と使い方（Usage）

### 5.1 動作環境

- **Python**：3.11 以上
- **依存パッケージ**：pytest、black、mypy、pytest-cov（`requirements.txt` 参照）

### 5.2 インストール

```bash
pip install -r requirements.txt
```

### 5.3 サンプルコード

```python
# サンプル：各データ構造の最小限の使用例 / Sample: Minimal usage of each data structure

from pydsai import ArrayList, DoublyLinkedList, Stack, Deque

# --- ArrayList：動的配列 / Dynamic array ---
arr = ArrayList()
arr.add(1)
arr.add(2)
print(arr.get(0))  # 出力: 1 / Output: 1

# --- DoublyLinkedList：双方向連結リスト / Doubly linked list ---
dll = DoublyLinkedList()
dll.add_first(1)
dll.add_last(2)
print(list(dll))  # 出力: [1, 2] / Output: [1, 2]

# --- Stack：スタック（LIFO）/ Stack (LIFO) ---
stack = Stack()
stack.push(1)
stack.push(2)
print(stack.pop())  # 出力: 2（後入れ先出し）/ Output: 2 (Last-In-First-Out)

# --- Deque：Queue モード（FIFO）/ Deque in Queue mode (FIFO) ---
queue = Deque()
queue.enqueue(1)
queue.enqueue(2)
print(queue.dequeue())  # 出力: 1（先入れ先出し）/ Output: 1 (First-In-First-Out)

# --- Deque：Stack モード（LIFO）/ Deque in Stack mode (LIFO) ---
stack2 = Deque()
stack2.push(1)
stack2.push(2)
print(stack2.pop())  # 出力: 2 / Output: 2

# --- Deque：両端操作 / Deque bidirectional operations ---
dq = Deque()
dq.add_first(1)
dq.add_last(2)
print(dq.peek_first(), dq.peek_last())  # 出力: 1 2 / Output: 1 2
```

---

## ⑥ 品質担保について

| 項目 | 実績 |
|------|------|
| **単体テスト** | **47 件**のテストケース（境界条件・空状態・並行書き込み・BST 含む）が 100% 通過 |
| **コードフォーマット** | Black（line length 88）に準拠 |
| **型チェック** | mypy strict mode を満たし、型アノテーションを全メソッドに付与 |
| **ドキュメント** | Javadoc 風 docstring（英語・日本語併記）をクラス・メソッドに適用 |

---

## ⑦ 今後の展望（Future Work）

- **平衡二分探索木（AVL 木 / Red-Black 木）**：BST の最悪 O(n) 劣化を解消し、保証付き O(log n) を実現
- **Read-Write Lock への最適化**：読み取りが多い局面での並行性向上のため、`threading.RLock` や読み書きロックの検討
- **優先度付きキュー（Priority Queue）**：ヒープによる実装の導入
- **ハッシュテーブル（Hash Table）**：O(1) 期待時間での検索・挿入・削除の実装

---

## パフォーマンスベンチマーク（Performance Benchmarking）

プロジェクトには `examples/performance_benchmark.py` が含まれる。以下の比較を実施可能：

- **Search**：ArrayList 線形検索 O(n) vs BinarySearchTree 検索 O(log n)（20,000 件）
- **Insert at head**：ArrayList.insert_at(0) O(n) vs Deque.add_first O(1)（20,000 回）
- **Iteration**：ArrayList vs LinkedList の全走査（空間的局所性の影響）

実行後、`benchmark_report.txt` に結果が保存される。

```bash
python examples/performance_benchmark.py
```

---

## スレッドセーフ監査（Thread-Safety Audit）

本プロジェクトでは、**インスタンス単位のロック（per-instance lock）** を採用している。

**設計理由**：

1. **排他範囲の明確化**：各データ構造インスタンスが独自の `threading.Lock` を保持するため、異なるインスタンス間でロック競合が発生せず、並行処理のスケーラビリティを確保できる。
2. **デッドロック回避**：単一ロックのみを使用するため、複数ロックの取得順序に起因するデッドロックが発生しない。
3. **原子性の担保**：`pop_last`、`peek_last`、`delete`（BST）など、複数ステップを要する操作をロック内で完結させることで、中間状態の露出を防いでいる。

**トレードオフ**：読み取りが多い局面では、Read-Write Lock による最適化の余地がある（今後の展望として `docs/COMPLEXITY.md` に記載）。

---

## 面接でアピールできるポイント

### CPU キャッシュ最適化

ArrayList は**連続メモリ**に要素を配置し、**空間的局所性（Spatial Locality）**を活かしている。CPU がキャッシュライン（通常 64 バイト）をロードする際、隣接要素も同時にキャッシュに載るため、逐次アクセス時のキャッシュヒット率が高い。一方、LinkedList はノードがメモリ上に分散するため、ランダムアクセスが多くなり、キャッシュミスが増加する。詳細は `docs/COMPLEXITY.md` の Deep Dive を参照されたい。

### アーキテクチャ設計の意図

- **LinearList 抽象化**：実装の差し替えや拡張を容易にするため、インターフェースを契約として定義した。
- **合成の採用**：Stack と Deque は、用途に応じて ArrayList や DoublyLinkedList を内部に組み合わせており、継承による過度な結合を避けている。

### スレッドセーフの担保方法

基底データ構造（ArrayList、DoublyLinkedList）に `threading.Lock` を導入し、すべてのメソッド呼び出しを排他制御している。`pop`・`peek` のような複数ステップを要する操作は、一つのロック内で完了する原子操作として実装し、中間状態の露出を防いでいる。

---

## ドキュメント・参照

- **計算量リファレンス**：[docs/COMPLEXITY.md](docs/COMPLEXITY.md)
- **GitHub 新規アカウントセットアップ**：[docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md)
- **プロジェクトバージョン**：0.1.0
