"""Stack test cases."""

from __future__ import annotations

import pytest

from pydsai.interfaces import LinearList
from pydsai.stack import Stack


def test_should_verify_lifo_behavior() -> None:
    # Arrange
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)

    # Act & Assert: Last-In-First-Out
    assert stack.pop() == 3
    assert stack.pop() == 2
    assert stack.pop() == 1


def test_should_raise_index_error_on_pop_empty_stack() -> None:
    # Arrange
    stack = Stack()

    # Act & Assert
    with pytest.raises(IndexError, match="empty"):
        stack.pop()


def test_should_raise_index_error_on_peek_empty_stack() -> None:
    # Arrange
    stack = Stack()

    # Act & Assert
    with pytest.raises(IndexError, match="empty"):
        stack.peek()


def test_should_handle_mixed_push_pop_operations() -> None:
    # Arrange
    stack = Stack()

    # Act & Assert
    stack.push(10)
    stack.push(20)
    assert stack.pop() == 20
    stack.push(30)
    stack.push(40)
    assert stack.peek() == 40
    assert stack.pop() == 40
    assert stack.pop() == 30
    assert stack.pop() == 10


def test_should_respect_linearlist_interface() -> None:
    # Arrange: Stack is a LinearList
    stack: LinearList = Stack()

    # Act: Use interface methods
    stack.add(1)
    stack.add(2)
    stack.add(3)

    # Assert
    assert stack.size() == 3
    assert stack.get(0) == 1
    assert stack.get(1) == 2
    assert stack.get(2) == 3

    removed = stack.remove(2)
    assert removed is True
    assert stack.size() == 2
    assert stack.get(0) == 1
    assert stack.get(1) == 3
