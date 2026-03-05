"""Dataobj → 解引用到具体的数据类型 转换器

DATAOBJ 引用一个数据类型对象（通过 dtref），需要获取已转换的数据类型模型，
然后用 DATAOBJ 自身的属性覆盖。
"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Dataobj, Name, Tuv
from ...models.base import CodedElement
from ...registry import ObjectRegistry


class DataobjTransformer(BaseTransformer):
    """将 Dataobj（数据对象）转换为对应的模型元素
    
    DATAOBJ 本身不产生新类型，而是解引用 dtref 获取数据类型，
    然后用自身属性覆盖生成新的元素对象。
    """

    priority = 60
    handles_type = Dataobj

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Dataobj)

    def transform(self, raw_obj: Dataobj, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> Any:
        # 递归确保引用的数据类型已转换
        ref_element = self._resolve_one(
            raw_obj.dtref, registry, warnings, strict,
            context=f"DATAOBJ {raw_obj.id or raw_obj.oid} ",
        )

        if ref_element is None:
            return None

        # 由于 frozen=True，需要用 dataclasses.replace 创建新对象并覆盖属性
        # 收集要覆盖的字段
        overrides = {}

        if raw_obj.name:
            overrides['name'] = raw_obj.name
        if raw_obj.qual:
            overrides['qualifier'] = raw_obj.qual
        if raw_obj.desc:
            overrides['description'] = raw_obj.desc
        if raw_obj.id:
            overrides['id'] = raw_obj.id
        elif raw_obj.oid:
            overrides['id'] = raw_obj.oid
        if raw_obj.v is not None:
            overrides['constvalue'] = raw_obj.v
        if raw_obj.spec:
            overrides['spec'] = raw_obj.spec

        # 使用 dataclasses.replace 创建新对象（保持 frozen 不可变性）
        import dataclasses
        try:
            element = dataclasses.replace(ref_element, **overrides)
        except (TypeError, dataclasses.FrozenInstanceError):
            # 如果 ref_element 不是 dataclass 或其他异常情况
            # 回退到直接返回引用并记录警告
            warnings.append(f"DATAOBJ {raw_obj.id or raw_obj.oid}: 无法覆盖引用对象属性")
            element = ref_element

        return element
