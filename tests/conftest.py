"""Pytest configuration: Add src to Python path for pydsai import.

Pytest 設定：pydsai のインポートのために src を Python パスに追加。
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add project src to path / プロジェクトの src をパスに追加
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "src"))
