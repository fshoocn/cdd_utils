"""具体元素类型 — 每种类型对应一种编码方式

所有元素都是不可变的 frozen dataclass。
"""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Optional, List, Any

from .base import CodedElement, IdentifiableElement
from .candela import Comp, Textmap
from ..codec.codec_utils import parse_textmap_s


@dataclass(frozen=True)
class ConstElement(CodedElement):
    """常量元素 — 固定值，用于 SID、SubFunction 等
    
    constvalue 存储固定的常量值。
    """
    pass


@dataclass(frozen=True)
class TextTableElement(CodedElement):
    """文本映射元素 — 原始值 ↔ 文本
    
    textmap 存储值到文本的映射关系。
    __post_init__ 自动将 textmap 中的 s/e 从元组字符串 '(31,0,0)' 规范化为整数。
    """
    textmap: tuple = ()

    def __post_init__(self):
        """规范化 textmap 中的 s/e 字段：元组字符串 '(31,0,0)' → 整数。

        为避免就地修改外部 Textmap 对象（破坏不可变性），
        对需要转换的条目创建浅拷贝后再修改。
        """
        normalized = []
        changed = False
        for tm in self.textmap:
            need_copy = False
            new_s, new_e = tm.s, tm.e
            if tm.s is not None and not isinstance(tm.s, int):
                new_s = parse_textmap_s(tm.s)
                need_copy = True
            if tm.e is not None and not isinstance(tm.e, int):
                new_e = parse_textmap_s(tm.e)
                need_copy = True
            if need_copy:
                tm_copy = copy.copy(tm)
                tm_copy.s = new_s
                tm_copy.e = new_e
                normalized.append(tm_copy)
                changed = True
            else:
                normalized.append(tm)
        if changed:
            # frozen dataclass 需要通过 object.__setattr__ 替换
            object.__setattr__(self, 'textmap', tuple(normalized))


@dataclass(frozen=True)
class LinCompElement(CodedElement):
    """线性转换元素 — 物理值 = 原始值 × factor + offset
    
    comp 存储线性转换参数 (f=因子, o=偏移量, s=起始值, e=结束值)。
    """
    comp: Optional[Comp] = None


@dataclass(frozen=True)
class PlaceholderElement(CodedElement):
    """占位元素 — 保留位/填充位
    
    用于填充信号中的保留位或未使用位。
    """
    pass
