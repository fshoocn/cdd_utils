"""Eositercomp → StructElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Eositercomp, Name, Tuv
from ...models.containers import StructElement
from ...registry import ObjectRegistry


class EositercompTransformer(BaseTransformer):
    """将 Eositercomp（结束标记迭代器组件）转换为 StructElement"""

    priority = 50
    handles_type = Eositercomp

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Eositercomp)

    def transform(self, raw_obj: Eositercomp, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> StructElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed EosIter Component"),
                 Tuv(lang="zh-CN", value="未命名迭代器组件")]
        )

        children = self._resolve_children(
            raw_obj.items, registry, warnings, strict,
            context="EOSITERCOMP ",
        )

        return StructElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            must=raw_obj.must,
            min_num_of_items=raw_obj.min_num_of_items if raw_obj.min_num_of_items is not None else 0,
            max_num_of_items=raw_obj.max_num_of_items,
            children=tuple(children),
        )
