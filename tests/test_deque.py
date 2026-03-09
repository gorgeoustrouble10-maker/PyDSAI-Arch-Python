"""Deque test cases."""

from __future__ import annotations

import pytest

from pydsai.interfaces import LinearList
from pydsai.deque import Deque


def test_should_verify_fifo_queue_behavior() -> None:
    # Arrange: Queue mode - enqueue at back, dequeue from front
    dq = Deque()
    dq.enqueue(1)
    dq.enqueue(2)
    dq.enqueue(3)

    # Act & Assert: First-In-First-Out
    assert dq.dequeue() == 1
    assert dq.dequeue() == 2
    assert dq.dequeue() == 3


def test_should_verify_lifo_stack_behavior() -> None:
    # Arrange: Stack mode - push and pop at back
    dq = Deque()
    dq.push(1)
    dq.push(2)
    dq.push(3)

    # Act & Assert: Last-In-First-Out
    assert dq.pop() == 3
    assert dq.pop() == 2
    assert dq.pop() == 1


def test_should_handle_bidirectional_operations() -> None:
    # Arrange
    dq = Deque()

    # Act: Add from both ends
    dq.add_first(2)
    dq.add_last(3)
    dq.add_first(1)
    dq.add_last(4)

    # Assert
    assert dq.peek_first() == 1
    assert dq.peek_last() == 4
    assert dq.remove_first() == 1
    assert dq.remove_last() == 4
    assert dq.remove_first() == 2
    assert dq.remove_last() == 3


def test_should_raise_index_error_on_empty_remove_first() -> None:
    # Arrange
    dq = Deque()

    # Act & Assert
    with pytest.raises(IndexError, match="empty"):
        dq.remove_first()


def test_should_raise_index_error_on_empty_remove_last() -> None:
    # Arrange
    dq = Deque()

    # Act & Assert
    with pytest.raises(IndexError, match="empty"):
        dq.remove_last()


def test_should_raise_index_error_on_empty_peek_first() -> None:
    # Arrange
    dq = Deque()

    # Act & Assert
    with pytest.raises(IndexError, match="empty"):
        dq.peek_first()


def test_should_raise_index_error_on_empty_peek_last() -> None:
    # Arrange
    dq = Deque()

    # Act & Assert
    with pytest.raises(IndexError, match="empty"):
        dq.peek_last()


def test_should_raise_index_error_on_empty_dequeue() -> None:
    # Arrange
    dq = Deque()

    # Act & Assert
    with pytest.raises(IndexError, match="empty"):
        dq.dequeue()


def test_should_raise_index_error_on_empty_pop() -> None:
    # Arrange
    dq = Deque()

    # Act & Assert
    with pytest.raises(IndexError, match="empty"):
        dq.pop()


def test_should_respect_linearlist_interface() -> None:
    # Arrange
    dq: LinearList = Deque()

    # Act
    dq.add(1)
    dq.add(2)
    dq.add(3)

    # Assert
    assert dq.size() == 3
    assert dq.get(0) == 1
    assert dq.get(1) == 2
    assert dq.get(2) == 3

    removed = dq.remove(2)
    assert removed is True
    assert dq.size() == 2
