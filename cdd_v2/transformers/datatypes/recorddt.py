"""Recorddt → TextTableElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Recorddt, Name, Tuv, Textmap
from ...models.elements import TextTableElement
from ...models.base import ByteOrder, DisplayFormat, Encoding, Quantity
from ...registry import ObjectRegistry


class RecorddtTransformer(BaseTransformer):
    """将 Recorddt（记录数据类型）转换为 TextTableElement"""

    priority = 50
    handles_type = Recorddt

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Recorddt)

    def transform(self, raw_obj: Recorddt, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> TextTableElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Record Data Type"),
                 Tuv(lang="zh-CN", value="记录数据类型")]
        )

        cval = raw_obj.cvaluetype
        bit_length = cval.bl if cval and cval.bl else 0
        byte_order = ByteOrder(str(cval.bo)) if cval and cval.bo else ByteOrder.BIG_ENDIAN
        encoding = Encoding(cval.enc) if cval and cval.enc else Encoding.UNSIGNED
        display_format = DisplayFormat(cval.df) if cval and cval.df else DisplayFormat.HEX
        quantity = Quantity(cval.qty) if cval and cval.qty else Quantity.ATOM
        sig = cval.sig if cval else None
        minsz = cval.minsz if cval and cval.minsz else 0
        maxsz = cval.maxsz if cval and cval.maxsz else 255

        textmap_list = []
        # 1. 内联 RECORD 条目
        for record in raw_obj.record:
            v = record.v if record.v is not None else 0
            text_content = record.text if record.text and record.text.tuv else None
            textmap_list.append(Textmap(s=v, e=v, text=text_content))

        # 2. RECORDREF 引用 — 解析 RECORDDTPOOL 中的 RECORD 条目
        for rref in raw_obj.recordref:
            ref_raw = registry.get_raw(rref.idref) if rref.idref else None
            if ref_raw is not None and hasattr(ref_raw, 'v'):
                v = ref_raw.v if ref_raw.v is not None else 0
                text_content = ref_raw.text if hasattr(ref_raw, 'text') and ref_raw.text and ref_raw.text.tuv else None
                textmap_list.append(Textmap(s=v, e=v, text=text_content))
            elif rref.idref:
                warnings.append(f"RECORDDT {raw_obj.id or raw_obj.oid}: RECORDREF {rref.idref} 未找到")

        return TextTableElement(
            id=raw_obj.oid,
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
            textmap=tuple(textmap_list),
        )
