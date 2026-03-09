"""Thread-safe dynamic array implementation.

スレッドセーフな動的配列の実装。
"""

from __future__ import annotations

import functools
import threading
from typing import Any, Callable, Iterator, TypeVar

from pydsai.interfaces import LinearList

F = TypeVar("F", bound=Callable[..., Any])

INITIAL_CAPACITY = 10


def log_operation(func: F) -> F:
    """Decorator: Print method name and arguments to console.

    デコレータ：メソッド名と引数をコンソールに出力する。

    Args:
        func: The function to decorate. デコレート対象の関数。

    Returns:
        Wrapped function preserving signature and return value.
        シグネチャと戻り値を保持したラップ関数。
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        args_repr = ", ".join(repr(a) for a in args[1:])  # 跳过 self
        if kwargs:
            kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            params = f"{args_repr}, {kwargs_repr}" if args_repr else kwargs_repr
        else:
            params = args_repr
        print(f"[log] {func.__name__}({params})")
        return func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


class ArrayList(LinearList):
    """Thread-safe dynamic array.

    スレッドセーフな動的配列。
    初期容量 10、満杯時に倍増。threading.Lock で全書き込みを保護。
    """

    def __init__(self) -> None:
        """Initialize empty array with initial capacity 10.

        初期容量 10 で空の配列を初期化する。
        """
        self._data: list[Any] = [None] * INITIAL_CAPACITY
        self._size = 0
        self._lock = threading.Lock()

    @log_operation
    def add(self, item: Any) -> None:
        """Append element to the end, expand if full. LinearList interface.

        末尾に要素を追加。満杯時は倍増。LinearList インターフェース対応。

        Args:
            item: The element to add. 追加する要素。
        """
        with self._lock:
            if self._size == len(self._data):
                self._expand()
            self._data[self._size] = item
            self._size += 1

    def append(self, item: Any) -> None:
        """Alias for add. Keeps backward compatibility.

        add のエイリアス。後方互換のため。
        """
        self.add(item)

    def insert_at(self, index: int, item: Any) -> None:
        """Insert item at index. O(n) due to shift.

        指定インデックスに要素を挿入する。シフトのため O(n)。

        Args:
            index: Insert position. 挿入位置。
            item: The element to insert. 挿入する要素。

        Raises:
            IndexError: If index out of range. インデックスが範囲外のとき。
        """
        with self._lock:
            if index < 0 or index > self._size:
                raise IndexError(f"Index {index} out of range (size={self._size})")
            if self._size == len(self._data):
                self._expand()
            for i in range(self._size, index, -1):
                self._data[i] = self._data[i - 1]
            self._data[index] = item
            self._size += 1

    def search(self, item: Any) -> bool:
        """Linear search. O(n).

        線形検索。O(n)。

        Args:
            item: The value to search for. 検索する値。

        Returns:
            True if found, False otherwise. 検出時 True、未検出時 False。
        """
        with self._lock:
            for i in range(self._size):
                if self._data[i] == item:
                    return True
            return False

    def _expand(self) -> None:
        """Double internal storage capacity. Caller must hold _lock.

        内部ストレージ容量を倍増。呼び出し側は _lock を保持すること。
        """
        new_capacity = len(self._data) * 2
        new_data: list[Any] = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data

    @log_operation
    def get(self, index: int) -> Any:
        """Get element at index.

        インデックスで要素を取得する。

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
            return self._data[index]

    @log_operation
    def remove(self, item: Any) -> bool:
        """Remove first element matching item. LinearList interface.

        最初に一致する要素を削除。LinearList インターフェース対応。

        Args:
            item: The value to remove. 削除する値。

        Returns:
            True if removed, False if not found. 削除成功時 True、未検出時 False。
        """
        with self._lock:
            for i in range(self._size):
                if self._data[i] == item:
                    self._delete_at_index(i)
                    return True
            return False

    def _delete_at_index(self, index: int) -> None:
        """Delete element at index. Caller must hold _lock.

        指定インデックスの要素を削除。呼び出し側は _lock を保持すること。
        """
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._data[self._size - 1] = None
        self._size -= 1

    def peek_last(self) -> Any:
        """Return last element without removing. Thread-safe.

        末尾要素を削除せずに返す。スレッドセーフ。

        Returns:
            The last element. 末尾の要素。

        Raises:
            IndexError: If array is empty. 配列が空のとき。
        """
        with self._lock:
            if self._size == 0:
                raise IndexError("Cannot peek from empty list")
            return self._data[self._size - 1]

    def pop_last(self) -> Any:
        """Remove and return last element. Thread-safe. For Stack etc.

        末尾要素を削除して返す。スレッドセーフ。Stack 等の合成クラス用。

        Returns:
            The last element. 末尾の要素。

        Raises:
            IndexError: If array is empty. 配列が空のとき。
        """
        with self._lock:
            if self._size == 0:
                raise IndexError("Cannot pop from empty list")
            last = self._data[self._size - 1]
            self._delete_at_index(self._size - 1)
            return last

    @log_operation
    def delete(self, index: int) -> None:
        """Delete element at index, shift following elements forward.

        指定インデックスの要素を削除し、以降の要素を前にシフトする。

        Args:
            index: Index of element to delete. 削除する要素のインデックス。

        Raises:
            IndexError: If index out of range. インデックスが範囲外のとき。
        """
        with self._lock:
            if index < 0 or index >= self._size:
                raise IndexError(f"Index {index} out of range (size={self._size})")
            self._delete_at_index(index)

    def __len__(self) -> int:
        """Return the number of elements. Supports len(lst).

        要素数を返す。len(lst) に対応。

        Returns:
            Number of elements. 配列内の要素数。
        """
        with self._lock:
            return self._size

    def __iter__(self) -> "Iterator[Any]":
        """Iterate over elements. Supports for x in lst.

        要素を順に走査。for x in lst に対応。

        Yields:
            Each element in order. 順番の各要素。
        """
        with self._lock:
            for i in range(self._size):
                yield self._data[i]

    def __getitem__(self, index: int) -> Any:
        """Get element at index. Supports lst[i].

        インデックスで要素を取得。lst[i] に対応。

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
            return self._data[index]

    @log_operation
    def size(self) -> int:
        """Return the number of elements.

        要素数を返す。

        Returns:
            Number of elements. 配列内の要素数。
        """
        with self._lock:
            return self._size

    @log_operation
    def __repr__(self) -> str:
        """Return string representation of the array.

        配列の文字列表現を返す。

        Returns:
            String like ArrayList([1, 2, 3]). ArrayList([1, 2, 3]) のような文字列。
        """
        with self._lock:
            elements = [self._data[i] for i in range(self._size)]
            return f"ArrayList({elements})"
