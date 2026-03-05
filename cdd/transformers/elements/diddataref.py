"""Diddataref/Didref → DidElement 转换器"""
from typing import Any, Union

from ..base import BaseTransformer
from ...compat import Diddataref, Didref, Did, Name, Tuv
from ...models.containers import DidElement
from ...registry import ObjectRegistry


class DiddatarefTransformer(BaseTransformer):
    """将 Diddataref/Didref（DID 数据引用）转换为 DidElement"""

    priority = 55
    handles_type = Diddataref

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, (Diddataref, Didref))

    def transform(self, raw_obj: Union[Diddataref, Didref], registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> DidElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed DID Data Reference"),
                 Tuv(lang="zh-CN", value="未命名 DID 数据引用")]
        )

        # 获取引用的 DID 对象（从注册表原始数据获取）
        did: Did = registry.get_raw(raw_obj.did_ref)
        desc = getattr(raw_obj, 'desc', None)

        if did is None:
            msg = f"找不到 DID 引用: {raw_obj.did_ref}"
            warnings.append(msg)
            return DidElement(
                id=raw_obj.oid,
                name=name,
                description=desc,
                qualifier=raw_obj.qual,
                did=0,
                children=(),
            )

        if raw_obj.name is None and did.name is not None:
            name = did.name
        if desc is None:
            desc = did.desc

        # 解析 DID 的 STRUCTURE 中的数据对象
        children = []
        if did.structure and did.structure.items:
            children = self._resolve_children(
                did.structure.items, registry, warnings, strict,
                context="DID ",
            )

        did_number = did.n if did.n is not None else 0

        return DidElement(
            id=raw_obj.oid,
            name=name,
            description=desc,
            qualifier=raw_obj.qual,
            did=did_number,
            children=tuple(children),
        )
