"""Binary Search Tree (BST) implementation.

二分探索木（BST）の実装。
"""

from __future__ import annotations

import threading
from collections import deque
from typing import Any, Optional

from pydsai.interfaces import Tree


class _TreeNode:
    """Internal node for Binary Search Tree.

    二分探索木の内部ノード。

    Attributes:
        val: Node value.
        left: Left child (smaller values).
        right: Right child (larger values).
    """

    def __init__(
        self,
        val: Any,
        left: Optional[_TreeNode] = None,
        right: Optional[_TreeNode] = None,
    ) -> None:
        """Initialize a tree node.

        木ノードを初期化する。

        Args:
            val: Node value.
            left: Left child.
            right: Right child.
        """
        self.val = val
        self.left = left
        self.right = right


class BinarySearchTree(Tree):
    """Thread-safe Binary Search Tree.

    スレッドセーフな二分探索木。

    Core properties (BST の基本性質):
    - Left subtree of a node contains only values < node.val.
    - Right subtree of a node contains only values >= node.val.
    - Both left and right subtrees are also BSTs.

    Time complexity (時間計算量):
    - Best/Average: O(log n) for insert, search, delete (balanced tree).
    - Worst: O(n) when the tree degrades to a linked list (e.g., inserting
      ascending order). This is a known limitation of plain BST without
      balancing (AVL, Red-Black).

    Hibbard Deletion: Uses inorder successor (min of right subtree) for
    replacement when deleting a node with two children. We choose successor
    over predecessor to maintain consistency with standard implementations
    (e.g., CLRS) and because the successor is trivial to find: the leftmost
    node of the right subtree has at most one child (no left child), simplifying
    the removal. Predecessor would be symmetric; both preserve BST property.
    """

    def __init__(self) -> None:
        """Initialize an empty BST.

        空の二分探索木を初期化する。
        """
        self._root: Optional[_TreeNode] = None
        self._size = 0
        self._lock = threading.Lock()

    def insert(self, val: Any) -> None:
        """Insert a value. Non-recursive (iterative) implementation.

        値を挿入する。非再帰（反復）実装。

        Recursive version (再帰版) for reference:
            def _insert_rec(node: Optional[_TreeNode], v: Any) -> _TreeNode:
                if node is None:
                    return _TreeNode(v)
                if v < node.val:
                    node.left = _insert_rec(node.left, v)
                else:
                    node.right = _insert_rec(node.right, v)
                return node

        Args:
            val: The value to insert.
        """
        with self._lock:
            new_node = _TreeNode(val)
            if self._root is None:
                self._root = new_node
                self._size += 1
                return

            curr = self._root
            while True:
                if val < curr.val:
                    if curr.left is None:
                        curr.left = new_node
                        self._size += 1
                        return
                    curr = curr.left
                else:
                    if curr.right is None:
                        curr.right = new_node
                        self._size += 1
                        return
                    curr = curr.right

    def search(self, val: Any) -> bool:
        """Search for a value. O(log n) average, O(n) worst case.

        値を検索する。平均 O(log n)、最悪 O(n)。

        Args:
            val: The value to search for.

        Returns:
            True if found, False otherwise.
        """
        with self._lock:
            curr = self._root
            while curr is not None:
                if val == curr.val:
                    return True
                if val < curr.val:
                    curr = curr.left
                else:
                    curr = curr.right
            return False

    def delete(self, val: Any) -> bool:
        """Delete a value using Hibbard deletion (inorder successor).

        Hibbard 削除（中順後継者）を用いて値を削除する。

        Three cases (3 ケース):
        1. Leaf node: Remove the node.
        2. One child: Replace node with its child.
        3. Two children: Replace with inorder successor (min of right subtree),
           then delete the successor node (which has at most one child).

        Args:
            val: The value to delete.

        Returns:
            True if deleted, False if not found.
        """
        with self._lock:
            parent: Optional[_TreeNode] = None
            curr = self._root
            is_left = False

            while curr is not None:
                if val == curr.val:
                    break
                parent = curr
                if val < curr.val:
                    curr = curr.left
                    is_left = True
                else:
                    curr = curr.right
                    is_left = False

            if curr is None:
                return False

            # Case 1: Leaf node
            if curr.left is None and curr.right is None:
                if parent is None:
                    self._root = None
                elif is_left:
                    parent.left = None
                else:
                    parent.right = None
                self._size -= 1
                return True

            # Case 2: One child
            if curr.left is None:
                child = curr.right
            elif curr.right is None:
                child = curr.left
            else:
                # Case 3: Two children - use inorder successor
                succ_parent = curr
                succ = curr.right
                while succ.left is not None:
                    succ_parent = succ
                    succ = succ.left

                curr.val = succ.val

                if succ_parent == curr:
                    succ_parent.right = succ.right
                else:
                    succ_parent.left = succ.right
                self._size -= 1
                return True

            if parent is None:
                self._root = child
            elif is_left:
                parent.left = child
            else:
                parent.right = child
            self._size -= 1
            return True

    def inorder_traversal(self) -> list[Any]:
        """Return inorder (LDR) traversal. Result is sorted ascending.

        中順走査（左・根・右）の結果を返す。昇順でソートされた結果になる。

        Returns:
            List of values in inorder order.
        """
        with self._lock:
            result: list[Any] = []

            def _inorder(node: Optional[_TreeNode]) -> None:
                if node is None:
                    return
                _inorder(node.left)
                result.append(node.val)
                _inorder(node.right)

            _inorder(self._root)
            return result

    def preorder_traversal(self) -> list[Any]:
        """Return preorder (DLR) traversal.

        前順走査（根・左・右）の結果を返す。

        Returns:
            List of values in preorder order.
        """
        with self._lock:
            result: list[Any] = []

            def _preorder(node: Optional[_TreeNode]) -> None:
                if node is None:
                    return
                result.append(node.val)
                _preorder(node.left)
                _preorder(node.right)

            _preorder(self._root)
            return result

    def postorder_traversal(self) -> list[Any]:
        """Return postorder (LRD) traversal.

        後順走査（左・右・根）の結果を返す。

        Returns:
            List of values in postorder order.
        """
        with self._lock:
            result: list[Any] = []

            def _postorder(node: Optional[_TreeNode]) -> None:
                if node is None:
                    return
                _postorder(node.left)
                _postorder(node.right)
                result.append(node.val)

            _postorder(self._root)
            return result

    def level_order_traversal(self) -> list[Any]:
        """Return level-order (BFS) traversal.

        レベル順走査（幅優先）の結果を返す。

        Returns:
            List of values in level order.
        """
        with self._lock:
            result: list[Any] = []
            if self._root is None:
                return result

            queue: deque[_TreeNode] = deque([self._root])
            while queue:
                node = queue.popleft()
                result.append(node.val)
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            return result

    def get_min(self) -> Any:
        """Get the minimum value (leftmost node).

        最小値（最も左のノード）を取得する。

        Returns:
            The minimum value.

        Raises:
            ValueError: If the tree is empty.
        """
        with self._lock:
            if self._root is None:
                raise ValueError("Cannot get_min from empty tree")
            curr = self._root
            while curr.left is not None:
                curr = curr.left
            return curr.val

    def get_max(self) -> Any:
        """Get the maximum value (rightmost node).

        最大値（最も右のノード）を取得する。

        Returns:
            The maximum value.

        Raises:
            ValueError: If the tree is empty.
        """
        with self._lock:
            if self._root is None:
                raise ValueError("Cannot get_max from empty tree")
            curr = self._root
            while curr.right is not None:
                curr = curr.right
            return curr.val

    def get_height(self) -> int:
        """Return tree height (max edges from root to leaf). Empty = -1.

        木の高さを返す（根から葉への最大辺数）。空は -1。

        Returns:
            Height. -1 if empty. 高さ。空なら -1。
        """
        with self._lock:
            return self._height_unsafe(self._root)

    def _height_unsafe(self, node: Optional[_TreeNode]) -> int:
        """Compute node height. Caller must hold _lock."""
        if node is None:
            return -1
        return (
            max(
                self._height_unsafe(node.left),
                self._height_unsafe(node.right),
            )
            + 1
        )

    def get_balance_factor(self) -> int:
        """Return root's balance factor: height(left) - height(right).

        根の平衡係数を返す：height(left) - height(right)。
        |bf| > 1 means unbalanced (AVL would rotate).

        Returns:
            Balance factor. 0 if empty. 平衡係数。空なら 0。
        """
        with self._lock:
            if self._root is None:
                return 0
            h_left = self._height_unsafe(self._root.left)
            h_right = self._height_unsafe(self._root.right)
            return h_left - h_right

    def visualize(self) -> None:
        """Print tree structure to console in a readable layout.

        コンソールに木構造を読みやすい形式で出力する。
        """
        with self._lock:
            lines: list[str] = []
            self._visualize_unsafe(self._root, "", True, lines)
            for line in lines:
                print(line)

    def _visualize_unsafe(
        self,
        node: Optional[_TreeNode],
        prefix: str,
        is_tail: bool,
        lines: list[str],
    ) -> None:
        """Build visualization lines. Caller must hold _lock."""
        if node is None:
            return
        conn = "└── " if is_tail else "├── "
        lines.append(prefix + conn + str(node.val))

        children: list[tuple[Optional[_TreeNode], bool]] = []
        if node.left is not None or node.right is not None:
            if node.left is not None:
                children.append((node.left, node.right is None))
            if node.right is not None:
                children.append((node.right, True))

        for i, (child, is_last) in enumerate(children):
            ext = "    " if is_tail else "│   "
            self._visualize_unsafe(
                child,
                prefix + ext,
                is_last,
                lines,
            )
