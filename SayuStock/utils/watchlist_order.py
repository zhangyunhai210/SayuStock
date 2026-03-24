"""
自选列表顺序的纯逻辑（便于单元测试，与数据库解耦）。

自选在库中以下划线拼接存储，展示顺序与拼接顺序一致。
"""

from typing import List, Tuple, Optional


def validate_full_reorder(
    current: List[str], ordered: List[str]
) -> Tuple[Optional[List[str]], Optional[str]]:
    """
    校验「排序自选」的完整顺序是否合法。

    :return: (新顺序, 错误说明)；合法时错误说明为 None。
    """
    if not current:
        return None, "当前无自选股票"
    if set(ordered) != set(current):
        return None, "排序列表须与当前自选股票完全一致（代码相同、数量相同）"
    if len(ordered) != len(current):
        return None, "排序列表存在重复或遗漏"
    return ordered, None


def swap_adjacent(
    current: List[str], index: int, delta: int
) -> Tuple[Optional[List[str]], Optional[str]]:
    """
    与相邻位置交换：delta=-1 表示与上一项交换（上移），+1 表示下移。
    """
    if not current:
        return None, "当前无自选股票"
    j = index + delta
    if index < 0 or index >= len(current):
        return None, "内部错误：索引越界"
    if j < 0:
        return None, "已经是第一个，无法上移"
    if j >= len(current):
        return None, "已经是最后一个，无法下移"
    new_list = list(current)
    new_list[index], new_list[j] = new_list[j], new_list[index]
    return new_list, None
