"""PyDSAI - AI-empowered Data Structures & Algorithms.

AI を活用したデータ構造・アルゴリズム実装。
"""

from pydsai.array_list import ArrayList, log_operation
from pydsai.bst import BinarySearchTree
from pydsai.deque import Deque
from pydsai.interfaces import LinearList, Tree
from pydsai.linked_list import DoublyLinkedList, Node
from pydsai.stack import Stack

__all__ = [
    "ArrayList",
    "BinarySearchTree",
    "Deque",
    "DoublyLinkedList",
    "LinearList",
    "Node",
    "Stack",
    "Tree",
    "log_operation",
    "__version__",
]
__version__ = "0.1.0"
