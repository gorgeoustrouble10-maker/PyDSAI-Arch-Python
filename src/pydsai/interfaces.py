"""Linear list abstract interface definition.

線形リスト抽象インターフェース定義。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class LinearList(ABC):
    """Linear list abstract base class.

    線形リスト抽象基底クラス。
    すべての実装クラスは add、remove、get、size を提供する必要がある。
    """

    @abstractmethod
    def add(self, item: Any) -> None:
        """Add an element to the linear list.

        線形リストに要素を追加する。

        Args:
            item: The element to add. 追加する要素。
        """
        ...

    @abstractmethod
    def remove(self, item: Any) -> bool:
        """Remove the specified element from the linear list.

        線形リストから指定要素を削除する。

        Args:
            item: The element to remove. 削除する要素。

        Returns:
            True if removed, False if not found.
            削除成功時 True、存在しない場合 False。
        """
        ...

    @abstractmethod
    def get(self, index: int) -> Any:
        """Get element at index.

        インデックスで要素を取得する。

        Args:
            index: Element index from 0. 0 始まりのインデックス。

        Returns:
            The element at the index. インデックス位置の要素。
        """
        ...

    @abstractmethod
    def size(self) -> int:
        """Return the number of elements.

        要素数を返す。

        Returns:
            Number of elements. 要素の個数。
        """
        ...


class Tree(ABC):
    """Tree abstract base class.

    木構造の抽象基底クラス。
    すべての実装クラスは insert、search、delete、inorder_traversal、get_min、get_max を提供する必要がある。
    """

    @abstractmethod
    def insert(self, val: Any) -> None:
        """Insert a value into the tree.

        木に値を挿入する。

        Args:
            val: The value to insert.
        """
        ...

    @abstractmethod
    def search(self, val: Any) -> bool:
        """Search for a value in the tree.

        木内で値を検索する。

        Args:
            val: The value to search for.

        Returns:
            True if found, False otherwise.
        """
        ...

    @abstractmethod
    def delete(self, val: Any) -> bool:
        """Delete a value from the tree.

        木から値を削除する。

        Args:
            val: The value to delete.

        Returns:
            True if deleted, False if not found.
        """
        ...

    @abstractmethod
    def inorder_traversal(self) -> list[Any]:
        """Return inorder (LDR) traversal result.

        中順走査（左・根・右）の結果を返す。

        Returns:
            List of values in inorder order.
        """
        ...

    @abstractmethod
    def get_min(self) -> Any:
        """Get the minimum value in the tree.

        木内の最小値を取得する。

        Returns:
            The minimum value.

        Raises:
            ValueError: If the tree is empty.
        """
        ...

    @abstractmethod
    def get_max(self) -> Any:
        """Get the maximum value in the tree.

        木内の最大値を取得する。

        Returns:
            The maximum value.

        Raises:
            ValueError: If the tree is empty.
        """
        ...
