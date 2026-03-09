"""Doubly linked list implementation.

双方向連結リストの実装。
"""

from __future__ import annotations

import threading
from typing import Any, Iterator, Optional

from pydsai.interfaces import LinearList


class Node:
    """Doubly linked list node.

    双方向連結リストのノード。

    Attributes:
        value: Node value. ノードに格納する値。
        prev: Previous node; None for head. 前のノード。先頭では None。
        next: Next node; None for tail. 次のノード。末尾では None。
    """

    def __init__(
        self,
        value: Any,
        prev: Optional[Node] = None,
        next: Optional[Node] = None,
    ) -> None:
        """Initialize a node.

        ノードを初期化する。

        Args:
            value: Node value. ノードの値。
            prev: Previous node. 前のノード。
            next: Next node. 次のノード。
        """
        self.value = value
        self.prev = prev
        self.next = next


class DoublyLinkedList(LinearList):
    """Doubly linked list. Thread-safe.

    双方向連結リスト。スレッドセーフ。
    head と tail ポインタを保持し、先頭・末尾挿入はともに O(1)。
    """

    def __init__(self) -> None:
        """Initialize an empty list.

        空のリストを初期化する。
        """
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._size = 0
        self._lock = threading.Lock()

    def add(self, item: Any) -> None:
        """Add element at end. LinearList interface. O(1).

        末尾に要素を追加。LinearList インターフェース対応。O(1)。
        """
        self.add_last(item)

    def add_first(self, value: Any) -> None:
        """Insert element at the head. O(1).

        先頭に要素を挿入。O(1)。

        Args:
            value: The value to insert. 挿入する値。
        """
        with self._lock:
            new_node = Node(value, prev=None, next=self._head)
            if self._head is None:
                self._head = new_node
                self._tail = new_node
            else:
                self._head.prev = new_node
                self._head = new_node
            self._size += 1

    def add_last(self, value: Any) -> None:
        """Insert element at the tail. O(1).

        末尾に要素を挿入。O(1)。

        Args:
            value: The value to insert. 挿入する値。
        """
        with self._lock:
            new_node = Node(value, prev=self._tail, next=None)
            if self._tail is None:
                self._head = new_node
                self._tail = new_node
            else:
                self._tail.next = new_node
                self._tail = new_node
            self._size += 1

    def peek_first(self) -> Any:
        """Return the first element without removing. Thread-safe.

        先頭要素を削除せずに返す。スレッドセーフ。
        """
        with self._lock:
            if self._head is None:
                raise IndexError("Cannot peek from empty list")
            return self._head.value

    def peek_last(self) -> Any:
        """Return the last element without removing. Thread-safe.

        末尾要素を削除せずに返す。スレッドセーフ。
        """
        with self._lock:
            if self._tail is None:
                raise IndexError("Cannot peek from empty list")
            return self._tail.value

    def pop_first(self) -> Any:
        """Remove and return the first element. Thread-safe.

        先頭要素を削除して返す。スレッドセーフ。
        """
        with self._lock:
            if self._head is None:
                raise IndexError("Cannot pop from empty list")
            node = self._head
            self._unlink_unsafe(node)
            return node.value

    def pop_last(self) -> Any:
        """Remove and return the last element. Thread-safe.

        末尾要素を削除して返す。スレッドセーフ。
        """
        with self._lock:
            if self._tail is None:
                raise IndexError("Cannot pop from empty list")
            node = self._tail
            self._unlink_unsafe(node)
            return node.value

    def get(self, index: int) -> Any:
        """Get element at index. O(n).

        インデックスで要素を取得。O(n)。

        Args:
            index: Element index from 0. 0 始まりのインデックス。

        Returns:
            The element at the index. インデックス位置の要素。

        Raises:
            IndexError: If index out of range. インデックスが範囲外のとき。
        """
        with self._lock:
            if index < 0 or index >= self._size:
                raise IndexError(f"Index {index} out of range (size={self._size})")
            curr = self._head
            for _ in range(index):
                if curr is None:
                    raise IndexError(f"Index {index} out of range (size={self._size})")
                curr = curr.next
            if curr is None:
                raise IndexError(f"Index {index} out of range (size={self._size})")
            return curr.value

    def size(self) -> int:
        """Return the number of elements. LinearList interface.

        要素数を返す。LinearList インターフェース対応。
        """
        with self._lock:
            return self._size

    def remove(self, value: Any) -> bool:
        """Remove first node matching value. LinearList interface.

        最初に一致するノードを削除。LinearList インターフェース対応。

        Args:
            value: The value to remove. 削除する値。

        Returns:
            True if removed, False if not found. 削除成功時 True、未検出時 False。
        """
        with self._lock:
            curr = self._head
            while curr is not None:
                if curr.value == value:
                    self._unlink_unsafe(curr)
                    return True
                curr = curr.next
            return False

    def _unlink_unsafe(self, node: Node) -> None:
        """Remove node from list. Caller must hold _lock.

        リストからノードを削除。呼び出し側は _lock を保持すること。

        Args:
            node: The node to remove. 削除するノード。
        """
        prev_node = node.prev
        next_node = node.next

        if prev_node is not None:
            prev_node.next = next_node
        else:
            self._head = next_node

        if next_node is not None:
            next_node.prev = prev_node
        else:
            self._tail = prev_node

        self._size -= 1

    def _iter_unsafe(self) -> Iterator[Any]:
        """Iterate over values. Caller must hold _lock.

        要素を走査。呼び出し側は _lock を保持すること。
        """
        curr = self._head
        while curr is not None:
            yield curr.value
            curr = curr.next

    def __iter__(self) -> Iterator[Any]:
        """Iterate from head to tail. Supports for-loop.

        先頭から末尾へ走査。for 文に対応。

        Yields:
            Value of each node. 各ノードの value。
        """
        with self._lock:
            snapshot = list(self._iter_unsafe())
        for v in snapshot:
            yield v

    def __repr__(self) -> str:
        """Return string representation of the list.

        リストの文字列表現を返す。

        Returns:
            String like DoublyLinkedList([1, 2, 3]). DoublyLinkedList([1, 2, 3]) のような文字列。
        """
        with self._lock:
            elements = list(self._iter_unsafe())
            return f"DoublyLinkedList({elements})"
