"""Ident → CodedElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Ident, Name, Tuv
from ...models.base import CodedElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ...registry import ObjectRegistry


class IdentTransformer(BaseTransformer):
    """将 Ident（标识符/数据类型）转换为 CodedElement"""

    priority = 50
    handles_type = Ident

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Ident)

    def transform(self, raw_obj: Ident, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> CodedElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed Ident"),
                 Tuv(lang="zh-CN", value="未命名Ident数据类型")]
        )

        return CodedElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            bit_length=raw_obj.cvaluetype.bl,
            display_format=raw_obj.pvaluetype.df,
            encoding=raw_obj.cvaluetype.enc,
            byte_order=ByteOrder(str(raw_obj.cvaluetype.bo).lower()),
            sig=raw_obj.cvaluetype.sig,
            quantity=raw_obj.cvaluetype.qty,
            minsz=raw_obj.cvaluetype.minsz,
            maxsz=raw_obj.cvaluetype.maxsz,
            excl=tuple(raw_obj.excl) if raw_obj.excl else (),
        )
