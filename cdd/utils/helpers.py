"""CDD V2 通用工具函数"""
from __future__ import annotations

from ..compat import Name, Tuv


def default_name(en: str, zh: str = "") -> Name:
    """创建默认 Name 对象

    减少转换器中重复的 Name(tuv=[Tuv(...)]) 样板代码。

    Args:
        en: 英文名称
        zh: 中文名称（可选）

    Returns:
        Name 对象
    """
    tuvs = [Tuv(lang="en-US", value=en)]
    if zh:
        tuvs.append(Tuv(lang="zh-CN", value=zh))
    return Name(tuv=tuvs)
