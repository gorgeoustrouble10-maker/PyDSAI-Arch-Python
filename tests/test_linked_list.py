"""DoublyLinkedList 测试用例。"""

from __future__ import annotations

import threading

import pytest

from pydsai.linked_list import DoublyLinkedList


def test_should_raise_index_error_when_get_out_of_bounds() -> None:
    # Arrange
    dll = DoublyLinkedList()
    dll.add_last(1)

    # Act & Assert
    with pytest.raises(IndexError, match="Index 1 out of range"):
        dll.get(1)

    with pytest.raises(IndexError, match="Index -1 out of range"):
        dll.get(-1)


def test_should_add_first_to_empty_list() -> None:
    # Arrange
    dll = DoublyLinkedList()

    # Act
    dll.add_first(1)

    # Assert
    assert list(dll) == [1]


def test_should_add_first_multiple_elements() -> None:
    # Arrange
    dll = DoublyLinkedList()

    # Act
    dll.add_first(1)
    dll.add_first(2)
    dll.add_last(3)

    # Assert
    assert list(dll) == [2, 1, 3]


def test_should_add_last_to_empty_list() -> None:
    # Arrange
    dll = DoublyLinkedList()

    # Act
    dll.add_last(1)

    # Assert
    assert list(dll) == [1]


def test_should_add_last_multiple_elements() -> None:
    # Arrange
    dll = DoublyLinkedList()

    # Act
    dll.add_last(1)
    dll.add_last(2)
    dll.add_last(3)

    # Assert
    assert list(dll) == [1, 2, 3]


def test_should_support_len_and_getitem() -> None:
    # Arrange
    dll = DoublyLinkedList()
    dll.add_last(1)
    dll.add_last(2)
    dll.add_last(3)

    # Assert __len__
    assert len(dll) == 3

    # Assert __getitem__
    assert dll[0] == 1
    assert dll[1] == 2
    assert dll[2] == 3


def test_should_add_via_interface_add_to_end() -> None:
    # Arrange: 验证 LinearList 接口 add() 等同于 add_last
    dll = DoublyLinkedList()

    # Act
    dll.add(1)
    dll.add(2)
    dll.add(3)

    # Assert
    assert list(dll) == [1, 2, 3]
    assert dll.size() == 3


def test_should_support_for_loop_iteration() -> None:
    # Arrange
    dll = DoublyLinkedList()
    dll.add_last(10)
    dll.add_last(20)
    dll.add_last(30)

    # Act
    result = [x for x in dll]

    # Assert
    assert result == [10, 20, 30]


def test_should_remove_head_element() -> None:
    # Arrange
    dll = DoublyLinkedList()
    dll.add_last(1)
    dll.add_last(2)
    dll.add_last(3)

    # Act
    removed = dll.remove(1)

    # Assert
    assert removed is True
    assert list(dll) == [2, 3]


def test_should_remove_tail_element() -> None:
    # Arrange
    dll = DoublyLinkedList()
    dll.add_last(1)
    dll.add_last(2)
    dll.add_last(3)

    # Act
    removed = dll.remove(3)

    # Assert
    assert removed is True
    assert list(dll) == [1, 2]


def test_should_remove_middle_element() -> None:
    # Arrange
    dll = DoublyLinkedList()
    dll.add_last(1)
    dll.add_last(2)
    dll.add_last(3)

    # Act
    removed = dll.remove(2)

    # Assert
    assert removed is True
    assert list(dll) == [1, 3]


def test_should_return_false_when_remove_nonexistent_value() -> None:
    # Arrange
    dll = DoublyLinkedList()
    dll.add_last(1)
    dll.add_last(2)

    # Act
    removed = dll.remove(99)

    # Assert
    assert removed is False
    assert list(dll) == [1, 2]


def test_should_remove_only_first_occurrence() -> None:
    # Arrange
    dll = DoublyLinkedList()
    dll.add_last(1)
    dll.add_last(2)
    dll.add_last(1)

    # Act
    removed = dll.remove(1)

    # Assert
    assert removed is True
    assert list(dll) == [2, 1]


def test_should_get_element_by_index_and_report_size() -> None:
    # Arrange
    dll = DoublyLinkedList()
    dll.add_last(10)
    dll.add_last(20)
    dll.add_last(30)

    # Act & Assert
    assert dll.size() == 3
    assert dll.get(0) == 10
    assert dll.get(1) == 20
    assert dll.get(2) == 30


def test_should_maintain_o1_head_tail_insertion_order() -> None:
    # Arrange: 交替头尾插入，验证顺序
    dll = DoublyLinkedList()

    # Act
    dll.add_first(3)
    dll.add_first(1)
    dll.add_last(4)
    dll.add_first(0)
    dll.add_last(5)
    dll.add_first(-1)
    dll.add_last(6)

    # Assert
    assert list(dll) == [-1, 0, 1, 3, 4, 5, 6]


def test_should_handle_concurrent_add_first_add_last() -> None:
    # Arrange
    dll = DoublyLinkedList()
    num_threads = 5
    items_per_thread = 100

    def add_from_both_ends(thread_id: int) -> None:
        for i in range(items_per_thread):
            dll.add_first((thread_id, "first", i))
            dll.add_last((thread_id, "last", i))

    # Act
    threads = [
        threading.Thread(target=add_from_both_ends, args=(i,))
        for i in range(num_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Assert
    assert dll.size() == num_threads * items_per_thread * 2
