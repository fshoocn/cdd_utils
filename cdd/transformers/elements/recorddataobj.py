"""Recorddataobj → TextTableElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Recorddataobj, Name, Tuv
from ...models.elements import TextTableElement
from ...registry import ObjectRegistry


class RecorddataobjTransformer(BaseTransformer):
    """将 Recorddataobj（记录数据对象）转换为 TextTableElement"""

    priority = 55
    handles_type = Recorddataobj

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Recorddataobj)

    def transform(self, raw_obj: Recorddataobj, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> TextTableElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Record Data Object"),
                 Tuv(lang="zh-CN", value="记录数据对象")]
        )

        if raw_obj.recorddt is None:
            warnings.append(f"RECORDDATAOBJ 缺少 RECORDDT: oid={raw_obj.oid}")
            return TextTableElement(
                id=raw_obj.oid,
                name=name,
                description=raw_obj.desc,
                qualifier=raw_obj.qual,
                spec=raw_obj.rt_spec,
                textmap=(),
            )

        # 内联转换 RECORDDT
        from ..transformer_registry import TransformerRegistry
        tr = TransformerRegistry()
        recorddt_element = tr.transform_one(raw_obj.recorddt, registry, warnings, strict)

        if recorddt_element is None:
            return TextTableElement(
                id=raw_obj.oid, name=name, spec=raw_obj.rt_spec, textmap=()
            )

        import dataclasses
        try:
            element = dataclasses.replace(
                recorddt_element,
                id=raw_obj.oid,
                name=name,
                description=raw_obj.desc or recorddt_element.description,
                qualifier=raw_obj.qual,
                spec=raw_obj.rt_spec,
            )
        except Exception:
            element = recorddt_element

        return element
