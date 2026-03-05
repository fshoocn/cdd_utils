"""Statusdtcproxycomp → CodedElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Statusdtcproxycomp, Name, Tuv
from ...models.base import CodedElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ...registry import ObjectRegistry


class StatusdtcproxycompTransformer(BaseTransformer):
    """将 Statusdtcproxycomp（DTC状态代理组件）转换为 CodedElement"""

    priority = 50
    handles_type = Statusdtcproxycomp

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Statusdtcproxycomp)

    def transform(self, raw_obj: Statusdtcproxycomp, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> CodedElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed Status DTC Proxy Component"),
                 Tuv(lang="zh-CN", value="未命名DTC状态代理组件")]
        )

        if raw_obj.minbl == raw_obj.maxbl and raw_obj.minbl is not None:
            bit_length = raw_obj.minbl
            minsz = 1
            maxsz = 1
            quantity = Quantity.ATOM
        else:
            bit_length = 1
            minsz = raw_obj.minbl
            maxsz = raw_obj.maxbl if raw_obj.maxbl is not None else raw_obj.minbl
            quantity = Quantity.FIELD

        return CodedElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec=raw_obj.dest,
            must=raw_obj.must,
            bit_length=bit_length,
            minsz=minsz,
            maxsz=maxsz,
            quantity=quantity,
            display_format=DisplayFormat.HEX,
            encoding=Encoding.UNSIGNED,
            byte_order=ByteOrder.BIG_ENDIAN,
        )
