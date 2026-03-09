"""Deque (double-ended queue) data structure implementation.

デック（両端キュー）データ構造の実装。
"""

from __future__ import annotations

from typing import Any

from pydsai.interfaces import LinearList
from pydsai.linked_list import DoublyLinkedList


class Deque(LinearList):
    """Thread-safe double-ended queue backed by DoublyLinkedList.

    スレッドセーフな両端キュー。内部で DoublyLinkedList を使用（合成による実装）。

    Supports Queue mode (FIFO) via enqueue/dequeue and Stack mode (LIFO) via push/pop.
    キューモード（FIFO）は enqueue/dequeue、スタックモード（LIFO）は push/pop で対応。

    Attributes:
        _storage: Internal DoublyLinkedList instance.
            Thread-safety via underlying list's lock.
    """

    def __init__(self) -> None:
        """Initialize an empty deque.

        空のデックを初期化する。
        """
        self._storage = DoublyLinkedList()

    def add_first(self, item: Any) -> None:
        """Insert element at the front.

        先頭に要素を追加する。

        Args:
            item: The element to add.
        """
        self._storage.add_first(item)

    def add_last(self, item: Any) -> None:
        """Insert element at the back.

        末尾に要素を追加する。

        Args:
            item: The element to add.
        """
        self._storage.add_last(item)

    def remove_first(self) -> Any:
        """Remove and return the front element.

        先頭要素を削除して返す。

        Returns:
            The front element.

        Raises:
            IndexError: If the deque is empty.
        """
        return self._storage.pop_first()

    def remove_last(self) -> Any:
        """Remove and return the back element.

        末尾要素を削除して返す。

        Returns:
            The back element.

        Raises:
            IndexError: If the deque is empty.
        """
        return self._storage.pop_last()

    def peek_first(self) -> Any:
        """Return the front element without removing.

        先頭要素を削除せずに返す。

        Returns:
            The front element.

        Raises:
            IndexError: If the deque is empty.
        """
        return self._storage.peek_first()

    def peek_last(self) -> Any:
        """Return the back element without removing.

        末尾要素を削除せずに返す。

        Returns:
            The back element.

        Raises:
            IndexError: If the deque is empty.
        """
        return self._storage.peek_last()

    # --- Queue mode (FIFO): enqueue at back, dequeue from front ---
    def enqueue(self, item: Any) -> None:
        """Add element to the back. Queue mode (FIFO).

        末尾に要素を追加。キューモード（FIFO）。

        Args:
            item: The element to add.
        """
        self.add_last(item)

    def dequeue(self) -> Any:
        """Remove and return the front element. Queue mode (FIFO).

        先頭要素を削除して返す。キューモード（FIFO）。

        Returns:
            The front element.
        """
        return self.remove_first()

    # --- Stack mode (LIFO): push at back, pop from back ---
    def push(self, item: Any) -> None:
        """Add element to the back. Stack mode (LIFO).

        末尾に要素を追加。スタックモード（LIFO）。

        Args:
            item: The element to add.
        """
        self.add_last(item)

    def pop(self) -> Any:
        """Remove and return the back element. Stack mode (LIFO).

        末尾要素を削除して返す。スタックモード（LIFO）。

        Returns:
            The back element.
        """
        return self.remove_last()

    # --- LinearList interface ---
    def add(self, item: Any) -> None:
        """Add element to the back. LinearList interface.

        LinearList インターフェース対応。末尾に追加。
        """
        self.add_last(item)

    def remove(self, item: Any) -> bool:
        """Remove first occurrence of element. LinearList interface.

        指定要素の最初の出現を削除。LinearList インターフェース対応。
        """
        return self._storage.remove(item)

    def get(self, index: int) -> Any:
        """Get element at index. LinearList interface.

        インデックスで要素を取得。LinearList インターフェース対応。
        """
        return self._storage.get(index)

    def size(self) -> int:
        """Return the number of elements. LinearList interface.

        要素数を返す。LinearList インターフェース対応。
        """
        return self._storage.size()
