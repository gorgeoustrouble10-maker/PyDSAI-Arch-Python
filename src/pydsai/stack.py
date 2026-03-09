"""Stack data structure implementation.

スタック（LIFO）データ構造の実装。
"""

from __future__ import annotations

from typing import Any

from pydsai.array_list import ArrayList
from pydsai.interfaces import LinearList


class Stack(LinearList):
    """Thread-safe LIFO (Last-In-First-Out) stack backed by ArrayList.

    スレッドセーフな LIFO スタック。内部で ArrayList を使用（合成による実装）。

    Attributes:
        _storage: Internal ArrayList instance for element storage.
            Thread-safety is ensured by the underlying ArrayList's lock.
    """

    def __init__(self) -> None:
        """Initialize an empty stack.

        空のスタックを初期化する。
        """
        self._storage = ArrayList()

    def push(self, item: Any) -> None:
        """Push an element onto the top of the stack.

        スタックの先頭に要素を追加する。

        Args:
            item: The element to push.

        """
        self._storage.add(item)

    def pop(self) -> Any:
        """Remove and return the top element of the stack.

        スタックの先頭要素を削除し、その値を返す。

        Returns:
            The top element.

        Raises:
            IndexError: If the stack is empty.
        """
        return self._storage.pop_last()

    def peek(self) -> Any:
        """Return the top element without removing it.

        スタックの先頭要素を削除せずに返す。

        Returns:
            The top element.

        Raises:
            IndexError: If the stack is empty.
        """
        return self._storage.peek_last()

    def add(self, item: Any) -> None:
        """Add an element. Delegates to push for LinearList interface.

        LinearList インターフェース対応。push に委譲する。

        Args:
            item: The element to add.
        """
        self.push(item)

    def remove(self, item: Any) -> bool:
        """Remove the first occurrence of an element.

        指定要素の最初の出現を削除する。LinearList インターフェース対応。

        Args:
            item: The element to remove.

        Returns:
            True if removed, False if not found.
        """
        return self._storage.remove(item)

    def get(self, index: int) -> Any:
        """Get element at index. Index 0 is bottom of stack.

        インデックスで要素を取得。0 はスタックの底を表す。

        Args:
            index: Element index from bottom (0-based).

        Returns:
            The element at the given index.
        """
        return self._storage.get(index)

    def size(self) -> int:
        """Return the number of elements in the stack.

        スタック内の要素数を返す。

        Returns:
            Number of elements.
        """
        return self._storage.size()
