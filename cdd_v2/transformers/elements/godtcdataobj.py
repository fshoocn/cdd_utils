"""Godtcdataobj → TextTableElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Godtcdataobj, Name, Tuv
from ...models.elements import TextTableElement
from ...registry import ObjectRegistry


class GodtcdataobjTransformer(BaseTransformer):
    """将 Godtcdataobj（DTC组数据对象）转换为 TextTableElement"""

    priority = 55
    handles_type = Godtcdataobj

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Godtcdataobj)

    def transform(self, raw_obj: Godtcdataobj, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> TextTableElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Group of DTC Data Object"),
                 Tuv(lang="zh-CN", value="DTC 组数据对象")]
        )

        if raw_obj.texttbl is None:
            warnings.append(f"GODTCDATAOBJ 缺少 TEXTTBL: oid={raw_obj.oid}")
            return TextTableElement(
                id=raw_obj.oid,
                name=name,
                description=raw_obj.desc,
                qualifier=raw_obj.qual,
                spec=raw_obj.spec,
                textmap=(),
            )

        # 内联转换 TEXTTBL
        from ..transformer_registry import TransformerRegistry
        tr = TransformerRegistry()
        texttbl_element = tr.transform_one(raw_obj.texttbl, registry, warnings, strict)

        if texttbl_element is None:
            return TextTableElement(
                id=raw_obj.oid, name=name, spec=raw_obj.spec, textmap=()
            )

        # 用 GODTCDATAOBJ 自身的元数据覆盖
        import dataclasses
        try:
            element = dataclasses.replace(
                texttbl_element,
                id=raw_obj.oid,
                name=name,
                description=raw_obj.desc or texttbl_element.description,
                qualifier=raw_obj.qual,
                spec=raw_obj.spec,
            )
        except Exception:
            element = texttbl_element

        return element
