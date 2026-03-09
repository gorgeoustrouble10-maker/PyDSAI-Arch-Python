"""ArrayList 测试用例。"""

from __future__ import annotations

import threading
from typing import Any

import pytest

from pydsai.array_list import ArrayList


def test_should_append_and_get_element() -> None:
    # Arrange
    arr = ArrayList()

    # Act
    arr.add(1)
    arr.add(2)
    arr.add(3)

    # Assert
    assert arr.get(0) == 1
    assert arr.get(1) == 2
    assert arr.get(2) == 3
    assert arr.size() == 3


def test_should_raise_index_error_when_get_out_of_bounds() -> None:
    # Arrange
    arr = ArrayList()
    arr.add(1)

    # Act & Assert
    with pytest.raises(IndexError, match="Index 1 out of range"):
        arr.get(1)

    with pytest.raises(IndexError, match="Index -1 out of range"):
        arr.get(-1)


def test_should_remove_element_by_value() -> None:
    # Arrange
    arr = ArrayList()
    arr.add(10)
    arr.add(20)
    arr.add(30)

    # Act
    removed = arr.remove(20)

    # Assert
    assert removed is True
    assert arr.size() == 2
    assert arr.get(0) == 10
    assert arr.get(1) == 30


def test_should_return_false_when_remove_nonexistent_value() -> None:
    # Arrange
    arr = ArrayList()
    arr.add(1)
    arr.add(2)

    # Act
    removed = arr.remove(99)

    # Assert
    assert removed is False
    assert arr.size() == 2


def test_should_expand_capacity_when_full() -> None:
    # Arrange
    arr = ArrayList()

    # Act: 添加 15 个元素，触发扩容
    for i in range(15):
        arr.add(i)

    # Assert
    assert arr.size() == 15
    for i in range(15):
        assert arr.get(i) == i


def test_should_support_len_getitem_iter() -> None:
    # Arrange
    arr = ArrayList()
    arr.add(10)
    arr.add(20)
    arr.add(30)

    # Assert __len__
    assert len(arr) == 3

    # Assert __getitem__
    assert arr[0] == 10
    assert arr[1] == 20
    assert arr[2] == 30

    # Assert __iter__
    assert list(arr) == [10, 20, 30]


def test_should_raise_index_error_on_getitem_out_of_bounds() -> None:
    arr = ArrayList()
    arr.add(1)
    with pytest.raises(IndexError, match="Index 1 out of range"):
        _ = arr[1]


def test_should_handle_concurrent_writes() -> None:
    # Arrange
    arr = ArrayList()
    num_threads = 5
    items_per_thread = 100

    def append_range(thread_id: int) -> None:
        for i in range(items_per_thread):
            arr.add((thread_id, i))

    # Act
    threads = [
        threading.Thread(target=append_range, args=(i,)) for i in range(num_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Assert
    assert arr.size() == num_threads * items_per_thread

    seen: set[tuple[int, int]] = set()
    for i in range(arr.size()):
        item: tuple[int, int] = arr.get(i)
        seen.add(item)

    assert len(seen) == num_threads * items_per_thread
    for thread_id in range(num_threads):
        for i in range(items_per_thread):
            assert (thread_id, i) in seen
