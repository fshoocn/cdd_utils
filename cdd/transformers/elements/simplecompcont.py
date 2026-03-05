"""Simplecompcont → StructElement 或单个元素 转换器"""
from typing import Any, Union

from ..base import BaseTransformer
from ...compat import Simplecompcont, Name, Tuv
from ...models.containers import StructElement
from ...models.base import CodedElement
from ...registry import ObjectRegistry


class SimplecompcontTransformer(BaseTransformer):
    """将 Simplecompcont（简单组件内容）转换为 StructElement 或单个元素"""

    priority = 55
    handles_type = Simplecompcont

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Simplecompcont)

    def transform(self, raw_obj: Simplecompcont, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> Any:
        children = self._resolve_children(
            raw_obj.items, registry, warnings, strict,
            context="SIMPLECOMPCONT ",
        )

        # 如果只有一个子元素，直接返回该元素
        if len(children) == 1:
            return children[0]

        name = Name(
            tuv=[Tuv(lang="en-US", value="Simple Component Content"),
                 Tuv(lang="zh-CN", value="简单组件内容")]
        )

        return StructElement(
            id=raw_obj.oid,
            name=name,
            spec=raw_obj.shproxyref,
            must=1,
            min_num_of_items=1,
            max_num_of_items=1,
            children=tuple(children),
        )
