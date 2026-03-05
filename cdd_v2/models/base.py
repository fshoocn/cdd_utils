"""基础元素类型 — 分层继承

设计原则:
- frozen=True → 构建后不可修改 → 共享引用安全 → 不需要 deepcopy
- IdentifiableElement: 所有有 ID 的元素基类 (6 个字段)
- CodedElement: 有编码属性的原子元素 (+编码相关字段)

容器类型 (Struct/Mux/NumIter) 继承 IdentifiableElement 而非 CodedElement，
因为容器本身没有 bit_length、encoding 等属性。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Any, TYPE_CHECKING
from enum import Enum

# 直接从同目录下的 candela.py (xsdata generated) 导入
from .candela import Name, Desc, Excl, Comp, Textmap


class ByteOrder(str, Enum):
    BIG_ENDIAN = "21"
    LITTLE_ENDIAN = "12"


class DisplayFormat(str, Enum):
    HEX = "hex"
    DECIMAL = "dec"
    TEXT = "text"
    BINARY = "bin"
    FLOAT = "flt"


class Encoding(str, Enum):
    UNSIGNED = "uns"
    SIGNED = "sgn"
    ASCII = "asc"
    UTF8 = "utf"
    BCD = "bcd"
    FLOAT = "flt"
    DOUBLE = "dbl"


class Quantity(str, Enum):
    ATOM = "atom"
    FIELD = "field"


@dataclass(frozen=True)
class IdentifiableElement:
    """所有有 ID 的元素的基类
    
    字段精简为 6 个，每个字段都有明确含义：
    - id: 全局唯一标识
    - name: 显示名称
    - description: 描述信息
    - qualifier: 限定符（用于属性访问）
    - spec: 规格说明 (如 'sid', 'sub', 'data', 'nrc' 等)
    - must: 是否必须 (0=可选, 1=必须)
    """
    name: Name
    id: Optional[str] = None
    description: Optional[Desc] = None
    qualifier: Optional[str] = None
    spec: Optional[str] = None
    must: Optional[int] = None


@dataclass(frozen=True)
class CodedElement(IdentifiableElement):
    """有编码属性的原子元素
    
    扩展了编码相关字段，用于叶子节点元素。
    isinstance(elem, CodedElement) 可区分叶子节点和容器节点。
    """
    constvalue: Optional[int] = None
    response_suppress_bit: Optional[int] = None

    bit_length: int = 0
    display_format: DisplayFormat = DisplayFormat.HEX
    encoding: Encoding = Encoding.UNSIGNED
    byte_order: ByteOrder = ByteOrder.BIG_ENDIAN
    sig: Optional[int] = None
    quantity: Quantity = Quantity.ATOM
    minsz: int = 1
    maxsz: int = 1

    excl: tuple = ()
    ref_id: Optional[str] = None
