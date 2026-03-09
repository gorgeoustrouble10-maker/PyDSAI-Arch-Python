#!/usr/bin/env python3
"""Format all Python files with Black and normalize to LF.

在推送前运行此脚本，确保与 CI 环境一致。
Usage: python scripts/format_and_normalize.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    # 1. Run black
    result = subprocess.run(
        [sys.executable, "-m", "black", "."],
        cwd=ROOT,
    )
    if result.returncode != 0:
        return result.returncode

    # 2. Normalize line endings to LF in all .py files
    for path in ROOT.rglob("*.py"):
        if ".git" in path.parts:
            continue
        data = path.read_bytes()
        if b"\r" in data:
            data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            path.write_bytes(data)

    print("Formatted and normalized to LF. Run: black . --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
