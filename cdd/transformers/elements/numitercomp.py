"""Numitercomp → NumIterElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Numitercomp, Name, Tuv, Simpleproxycomp
from ...models.containers import NumIterElement
from ...registry import ObjectRegistry


class NumitercompTransformer(BaseTransformer):
    """将 Numitercomp（数字迭代器组件）转换为 NumIterElement"""

    priority = 50
    handles_type = Numitercomp

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Numitercomp)

    def transform(self, raw_obj: Numitercomp, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> NumIterElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed NumIter Component"),
                 Tuv(lang="zh-CN", value="未命名数字迭代器组件")]
        )

        # 解析子组件
        children = []
        if raw_obj.simpleproxycomp is not None:
            # 内嵌 SIMPLEPROXYCOMP，需要内联转换
            from .simpleproxycomp import SimpleproxycompTransformer
            proxy_transformer = SimpleproxycompTransformer()
            child = proxy_transformer.transform(raw_obj.simpleproxycomp, registry, warnings, strict)
            if child is not None:
                children.append(child)

        return NumIterElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            must=raw_obj.must if raw_obj.must is not None else 1,
            selref=raw_obj.selref,
            selbm=raw_obj.selbm,
            children=tuple(children),
        )
