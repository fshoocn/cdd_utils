"""Contentcomp → StructElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Contentcomp, Name, Tuv
from ...models.containers import StructElement
from ...registry import ObjectRegistry


class ContentcompTransformer(BaseTransformer):
    """将 Contentcomp（内容组件）转换为 StructElement"""

    priority = 50
    handles_type = Contentcomp

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Contentcomp)

    def transform(self, raw_obj: Contentcomp, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> StructElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed Content Component"),
                 Tuv(lang="zh-CN", value="未命名内容组件")]
        )

        children = []
        if raw_obj.simplecompcont:
            children = self._resolve_children(
                raw_obj.simplecompcont.items, registry, warnings, strict,
                context="CONTENTCOMP ",
            )

        return StructElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            must=raw_obj.must if raw_obj.must is not None else 1,
            min_num_of_items=1,
            max_num_of_items=1,
            children=tuple(children),
        )
