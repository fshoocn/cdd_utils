"""Gapdataobj → PlaceholderElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Gapdataobj, Name, Tuv
from ...models.elements import PlaceholderElement
from ...registry import ObjectRegistry


class GapdataobjTransformer(BaseTransformer):
    """将 Gapdataobj（占位数据对象）转换为 PlaceholderElement"""

    priority = 50
    handles_type = Gapdataobj

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Gapdataobj)

    def transform(self, raw_obj: Gapdataobj, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> PlaceholderElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Gap Data"),
                 Tuv(lang="zh-CN", value="占位数据")]
        )

        bit_length = raw_obj.bl if raw_obj.bl is not None else 0

        return PlaceholderElement(
            id=raw_obj.oid,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            bit_length=bit_length,
            spec="no",
        )
