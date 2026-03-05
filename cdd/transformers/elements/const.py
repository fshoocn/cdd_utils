"""Constcomp → ConstElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Constcomp, Name, Tuv
from ...models.elements import ConstElement
from ...models.base import ByteOrder, DisplayFormat, Encoding, Quantity
from ...registry import ObjectRegistry


class ConstcompTransformer(BaseTransformer):
    """将 Constcomp（常量组件）转换为 ConstElement"""

    priority = 50
    handles_type = Constcomp

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Constcomp)

    def transform(self, raw_obj: Constcomp, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> ConstElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed Const Component"),
                 Tuv(lang="zh-CN", value="未命名常量组件")]
        )

        response_suppress_bit = None
        if raw_obj.spec == 'sub' and raw_obj.respsupbit is not None:
            response_suppress_bit = raw_obj.respsupbit

        return ConstElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec=raw_obj.spec,
            bit_length=raw_obj.bl if raw_obj.bl is not None else 8,
            constvalue=raw_obj.v if raw_obj.v is not None else 0,
            must=raw_obj.must if raw_obj.must is not None else 1,
            response_suppress_bit=response_suppress_bit,
            display_format=DisplayFormat.HEX,
            encoding=Encoding.UNSIGNED,
            byte_order=ByteOrder.BIG_ENDIAN,
            quantity=Quantity.ATOM,
        )
