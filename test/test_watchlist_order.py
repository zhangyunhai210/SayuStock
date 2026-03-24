"""自选顺序纯逻辑单元测试（不依赖 gsuid_core / 数据库）。

通过 importlib 直接加载模块，避免 import SayuStock 时执行 __init__.py。
"""

import importlib.util
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_MOD_PATH = _ROOT / "SayuStock" / "utils" / "watchlist_order.py"
_spec = importlib.util.spec_from_file_location("watchlist_order_standalone", _MOD_PATH)
assert _spec and _spec.loader
_watchlist_order = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_watchlist_order)
validate_full_reorder = _watchlist_order.validate_full_reorder
swap_adjacent = _watchlist_order.swap_adjacent


def test_validate_full_reorder_ok():
    cur = ["a", "b", "c"]
    ordered = ["c", "a", "b"]
    out, err = validate_full_reorder(cur, ordered)
    assert err is None
    assert out == ["c", "a", "b"]


def test_validate_full_reorder_empty_current():
    out, err = validate_full_reorder([], ["a"])
    assert out is None
    assert err is not None


def test_validate_full_reorder_mismatch():
    out, err = validate_full_reorder(["a", "b"], ["a", "c"])
    assert out is None
    assert err is not None


def test_swap_adjacent_up():
    cur = ["a", "b", "c"]
    out, err = swap_adjacent(cur, 1, -1)
    assert err is None
    assert out == ["b", "a", "c"]


def test_swap_adjacent_down():
    cur = ["a", "b", "c"]
    out, err = swap_adjacent(cur, 1, 1)
    assert err is None
    assert out == ["a", "c", "b"]


def test_swap_adjacent_boundary_top():
    out, err = swap_adjacent(["a", "b"], 0, -1)
    assert out is None
    assert err is not None


def test_swap_adjacent_boundary_bottom():
    out, err = swap_adjacent(["a", "b"], 1, 1)
    assert out is None
    assert err is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
