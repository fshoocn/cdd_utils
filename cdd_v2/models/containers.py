"""容器型元素 — 内部包含子元素

容器类型继承 IdentifiableElement（不继承 CodedElement），
因为容器本身没有 bit_length、encoding 等编码属性。
子元素用 tuple 而非 list（配合 frozen=True）。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Any, Union

from .base import IdentifiableElement, CodedElement
from .candela import Name, Desc


@dataclass(frozen=True)
class StructElement(IdentifiableElement):
    """结构体元素 — 有序子元素序列
    
    min_num_of_items / max_num_of_items 用于可重复结构（如 EOSITERCOMP）。
    """
    min_num_of_items: int = 1
    max_num_of_items: Optional[int] = 1
    children: tuple = ()
    ref_id: Optional[str] = None


@dataclass(frozen=True)
class MuxCase:
    """多路复用分支"""
    s: int
    e: int
    structure: StructElement


@dataclass(frozen=True)
class MultiplexedElement(IdentifiableElement):
    """多路复用元素 — 根据选择器值选择不同分支
    
    ref_textmap: 选择器引用的文本映射
    cases: 条件分支列表
    structure: 默认分支结构
    """
    ref_textmap: Any = None
    cases: tuple = ()
    structure: Optional[StructElement] = None
    ref_id: Optional[str] = None
    # 编码属性（从关联的 MUXDT 继承时可使用）
    bit_length: int = 0
    display_format: Any = None
    encoding: Any = None
    byte_order: Any = None


@dataclass(frozen=True)
class NumIterElement(IdentifiableElement):
    """数字迭代器元素 — count 决定 body 重复次数
    
    selref: 选择器引用 ID
    selbm: 选择器位掩码
    children: 迭代体元素
    """
    selref: Optional[str] = None
    selbm: Optional[int] = None
    children: tuple = ()


@dataclass(frozen=True)
class RecordElement(StructElement):
    """记录元素 — 带记录号的结构体"""
    record_number: int = 0


@dataclass(frozen=True)
class DidElement(IdentifiableElement):
    """DID 元素 — Data Identifier"""
    did: int = 0
    children: tuple = ()
