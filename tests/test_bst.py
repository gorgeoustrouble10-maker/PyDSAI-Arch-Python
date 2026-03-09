"""Binary Search Tree test cases."""

from __future__ import annotations

import threading

import pytest

from pydsai.bst import BinarySearchTree
from pydsai.interfaces import Tree


def test_should_support_contains_and_iter() -> None:
    # Arrange
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)

    # Assert __contains__
    assert 50 in bst
    assert 30 in bst
    assert 99 not in bst

    # Assert __iter__ (in-order)
    assert list(bst) == [30, 50, 70]


def test_should_insert_and_search_normal_values() -> None:
    # Arrange
    bst = BinarySearchTree()

    # Act
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(40)
    bst.insert(60)
    bst.insert(80)

    # Assert
    assert bst.search(50) is True
    assert bst.search(30) is True
    assert bst.search(70) is True
    assert bst.search(20) is True
    assert bst.search(40) is True
    assert bst.search(60) is True
    assert bst.search(80) is True
    assert bst.search(99) is False
    assert bst.search(0) is False


def test_should_verify_inorder_traversal_is_sorted_ascending() -> None:
    # Arrange
    bst = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80]

    # Act
    for v in values:
        bst.insert(v)
    inorder = bst.inorder_traversal()

    # Assert
    assert inorder == [20, 30, 40, 50, 60, 70, 80]


def test_should_delete_leaf_node() -> None:
    # Arrange
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)

    # Act
    deleted = bst.delete(20)

    # Assert
    assert deleted is True
    assert bst.search(20) is False
    assert bst.inorder_traversal() == [30, 50, 70]


def test_should_delete_node_with_one_child() -> None:
    # Arrange
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(25)  # Only child of 20

    # Act
    deleted = bst.delete(20)

    # Assert
    assert deleted is True
    assert bst.search(20) is False
    assert bst.inorder_traversal() == [25, 30, 50, 70]


def test_should_delete_node_with_two_children() -> None:
    # Arrange
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(40)
    bst.insert(35)
    bst.insert(45)

    # Act: Delete 30 (has left 20, right 40)
    deleted = bst.delete(30)

    # Assert: Inorder successor of 30 is 35 (min of right subtree)
    assert deleted is True
    assert bst.search(30) is False
    assert bst.inorder_traversal() == [20, 35, 40, 45, 50, 70]


def test_should_delete_root_node() -> None:
    # Arrange
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)

    # Act
    deleted = bst.delete(50)

    # Assert
    assert deleted is True
    assert bst.search(50) is False
    assert bst.inorder_traversal() == [30, 70]

    # Delete until empty
    bst.delete(30)
    bst.delete(70)
    assert bst.inorder_traversal() == []


def test_should_handle_empty_tree_operations() -> None:
    # Arrange
    bst = BinarySearchTree()

    # Act & Assert
    assert bst.search(1) is False
    assert bst.delete(1) is False
    assert bst.inorder_traversal() == []

    with pytest.raises(ValueError, match="empty"):
        bst.get_min()

    with pytest.raises(ValueError, match="empty"):
        bst.get_max()


def test_should_handle_duplicate_values() -> None:
    # Arrange: Duplicates go to right subtree
    bst = BinarySearchTree()
    bst.insert(5)
    bst.insert(5)
    bst.insert(5)

    # Act
    inorder = bst.inorder_traversal()
    found = bst.search(5)

    # Assert
    assert found is True
    assert inorder == [5, 5, 5]

    # Delete one occurrence
    bst.delete(5)
    assert bst.inorder_traversal() == [5, 5]


def test_should_get_min_and_max() -> None:
    # Arrange
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(80)

    # Act
    min_val = bst.get_min()
    max_val = bst.get_max()

    # Assert
    assert min_val == 20
    assert max_val == 80


def test_should_verify_preorder_postorder_level_order() -> None:
    # Arrange
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(40)
    bst.insert(60)
    bst.insert(80)

    # Assert
    assert bst.preorder_traversal() == [50, 30, 20, 40, 70, 60, 80]
    assert bst.postorder_traversal() == [20, 40, 30, 60, 80, 70, 50]
    assert bst.level_order_traversal() == [50, 30, 70, 20, 40, 60, 80]


def test_should_respect_tree_interface() -> None:
    # Arrange
    tree: Tree = BinarySearchTree()

    # Act
    tree.insert(1)
    tree.insert(2)
    tree.insert(3)

    # Assert
    assert tree.search(2) is True
    assert tree.inorder_traversal() == [1, 2, 3]
    assert tree.get_min() == 1
    assert tree.get_max() == 3
    tree.delete(2)
    assert tree.search(2) is False


def test_should_handle_degenerate_bst_without_recursion_error() -> None:
    # Arrange: Degenerate BST (chain) with 1500 nodes exceeds default recursion limit
    bst = BinarySearchTree()
    for i in range(1500):
        bst.insert(i)

    # Act & Assert: Must not raise RecursionError
    height = bst.get_height()
    bf = bst.get_balance_factor()

    assert height == 1499
    assert bf == -1499  # All nodes on right: height(left)=-1, height(right)=1498


def test_should_handle_concurrent_insert_and_search() -> None:
    # Arrange
    bst = BinarySearchTree()
    insert_values = list(range(100))
    search_values = list(range(100))

    def insert_many() -> None:
        for v in insert_values:
            bst.insert(v)

    def search_many() -> None:
        for v in search_values:
            _ = bst.search(v)

    # Act: Concurrent insert and search
    t1 = threading.Thread(target=insert_many)
    t2 = threading.Thread(target=search_many)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Assert: All values eventually present
    for v in insert_values:
        assert bst.search(v) is True
    assert bst.inorder_traversal() == sorted(insert_values)
