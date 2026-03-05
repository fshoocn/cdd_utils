"""Lincomp → LinCompElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Lincomp, Name, Tuv
from ...models.elements import LinCompElement
from ...models.base import ByteOrder, DisplayFormat, Encoding, Quantity
from ...registry import ObjectRegistry


class LincompTransformer(BaseTransformer):
    """将 Lincomp（线性转换组件）转换为 LinCompElement"""

    priority = 50
    handles_type = Lincomp

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Lincomp)

    def transform(self, raw_obj: Lincomp, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> LinCompElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed Linear Component"),
                 Tuv(lang="zh-CN", value="未命名线性转换组件")]
        )

        cval = raw_obj.cvaluetype
        bit_length = cval.bl if cval and cval.bl is not None else 8
        byte_order = ByteOrder(str(cval.bo)) if cval and cval.bo else ByteOrder.BIG_ENDIAN
        encoding = Encoding(cval.enc) if cval and cval.enc else Encoding.UNSIGNED
        display_format = DisplayFormat(raw_obj.pvaluetype.df) if raw_obj.pvaluetype and raw_obj.pvaluetype.df else DisplayFormat.DECIMAL
        quantity = Quantity(cval.qty) if cval and cval.qty else Quantity.ATOM
        sig = cval.sig if cval else None
        minsz = cval.minsz if cval and cval.minsz is not None else 1
        maxsz = cval.maxsz if cval and cval.maxsz is not None else 1

        excl_list = tuple(raw_obj.excl) if raw_obj.excl else ()

        return LinCompElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            bit_length=bit_length,
            byte_order=byte_order,
            encoding=encoding,
            display_format=display_format,
            quantity=quantity,
            sig=sig,
            minsz=minsz,
            maxsz=maxsz,
            excl=excl_list,
            comp=raw_obj.comp,
        )
