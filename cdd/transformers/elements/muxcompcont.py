"""Muxcompcont → 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Muxcompcont
from ...registry import ObjectRegistry


class MuxcompcontTransformer(BaseTransformer):
    """将 Muxcompcont（多路复用组件容器）转换为子元素
    
    MUXCOMPCONT 是一个透明容器，包含 MUXDT 或 DATAOBJ。
    """

    priority = 50
    handles_type = Muxcompcont

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Muxcompcont)

    def transform(self, raw_obj: Muxcompcont, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> Any:
        from ..transformer_registry import TransformerRegistry
        tr = TransformerRegistry()

        if raw_obj.muxdt:
            element = tr.transform_one(raw_obj.muxdt, registry, warnings, strict)
            if element is not None:
                return element

        if raw_obj.dataobj:
            element = tr.transform_one(raw_obj.dataobj, registry, warnings, strict)
            if element is not None:
                return element

        msg = f"MUXCOMPCONT 为空或解析失败: oid={raw_obj.oid}"
        warnings.append(msg)
        return None
