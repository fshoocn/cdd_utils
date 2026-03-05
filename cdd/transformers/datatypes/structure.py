"""Structure / Struct → StructElement 转换器"""
from typing import Any, Union

from ..base import BaseTransformer
from ...compat import Structure, Struct, Name, Tuv
from ...models.containers import StructElement
from ...registry import ObjectRegistry


class StructureTransformer(BaseTransformer):
    """将 Structure/Struct 转换为 StructElement
    
    - STRUCTURE: 纯容器，只有 items 列表
    - STRUCT: 结构体引用，有完整元数据和 items 列表
    """

    priority = 50

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, (Structure, Struct))

    def transform(self, raw_obj: Union[Structure, Struct], registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> StructElement:
        children = self._resolve_children(
            raw_obj.items or [], registry, warnings, strict,
            context="Structure ",
        )

        if isinstance(raw_obj, Struct):
            name = raw_obj.name or Name(
                tuv=[Tuv(lang="en-US", value="Unnamed Struct"),
                     Tuv(lang="zh-CN", value="未命名结构体")]
            )
            return StructElement(
                id=raw_obj.oid,
                name=name,
                description=raw_obj.desc,
                qualifier=raw_obj.qual,
                spec=raw_obj.spec,
                ref_id=raw_obj.dtref,
                children=tuple(children),
            )
        else:
            return StructElement(
                name=Name(
                    tuv=[Tuv(lang="en-US", value="Structure"),
                         Tuv(lang="zh-CN", value="结构体")]
                ),
                children=tuple(children),
            )
