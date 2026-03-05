"""Texttbl → TextTableElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Texttbl, Name, Tuv
from ...models.elements import TextTableElement
from ...models.base import ByteOrder, DisplayFormat, Encoding, Quantity
from ...registry import ObjectRegistry


class TexttblTransformer(BaseTransformer):
    """将 Texttbl（文本表）转换为 TextTableElement"""

    priority = 50
    handles_type = Texttbl

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Texttbl)

    def transform(self, raw_obj: Texttbl, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> TextTableElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed Text Table"),
                 Tuv(lang="zh-CN", value="未命名文本表")]
        )

        return TextTableElement(
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
            textmap=tuple(raw_obj.textmap) if raw_obj.textmap else (),
        )
