"""Specdataobj → TextTableElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Specdataobj, Name, Tuv, Textmap, Text, Negrescode
from ...models.elements import TextTableElement
from ...models.base import ByteOrder, DisplayFormat, Encoding, Quantity
from ...registry import ObjectRegistry


class SpecdataobjTransformer(BaseTransformer):
    """将 Specdataobj（特殊数据对象）转换为 TextTableElement
    
    SPECDATAOBJ 通常用于定义负响应码列表。
    """

    priority = 55
    handles_type = Specdataobj

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Specdataobj)

    def transform(self, raw_obj: Specdataobj, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> TextTableElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Negative Response Codes"),
                 Tuv(lang="zh-CN", value="负响应码列表")]
        )

        textmap_list = []
        if raw_obj.negrescodeproxies and raw_obj.negrescodeproxies.negrescodeproxy:
            for proxy in raw_obj.negrescodeproxies.negrescodeproxy:
                if proxy.idref:
                    negrescode: Negrescode = registry.get_raw(proxy.idref)
                    if negrescode is None:
                        warnings.append(f"找不到 NEGRESCODE 引用: {proxy.idref}")
                        continue
                    textmap = Textmap(
                        s=negrescode.v,
                        e=negrescode.v,
                        text=Text(tuv=negrescode.name.tuv) if negrescode.name else None,
                        addinfo=None
                    )
                    textmap_list.append(textmap)

        return TextTableElement(
            id=raw_obj.oid,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec="nrc",
            bit_length=8,
            display_format=DisplayFormat.HEX,
            encoding=Encoding.UNSIGNED,
            byte_order=ByteOrder.BIG_ENDIAN,
            quantity=Quantity.ATOM,
            textmap=tuple(textmap_list),
        )
