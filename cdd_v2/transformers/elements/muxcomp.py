"""Muxcomp → MultiplexedElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Muxcomp, Name, Tuv
from ...models.containers import MultiplexedElement
from ...registry import ObjectRegistry


class MuxcompTransformer(BaseTransformer):
    """将 Muxcomp（多路复用组件）转换为 MultiplexedElement
    
    MUXCOMP 引用 MUXDT（通过 dest 属性），需要获取已转换的 MUXDT 模型。
    """

    priority = 50
    handles_type = Muxcomp

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Muxcomp)

    def transform(self, raw_obj: Muxcomp, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> MultiplexedElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Multiplexed Component"),
                 Tuv(lang="zh-CN", value="多路复用组件")]
        )

        # 递归确保 MUXDT 已转换
        mux_element = self._resolve_one(
            raw_obj.dest, registry, warnings, strict,
            context=f"MUXCOMP {raw_obj.oid} ",
        ) if raw_obj.dest else None

        if mux_element is None:
            msg = f"MUXCOMP {raw_obj.oid} 引用目标未找到: dest={raw_obj.dest}"
            warnings.append(msg)
            return MultiplexedElement(
                id=raw_obj.oid,
                name=name,
                description=raw_obj.desc,
                qualifier=raw_obj.qual,
            )

        # 构建新的 MultiplexedElement，融合 MUXCOMP + MUXDT 的属性
        return MultiplexedElement(
            id=raw_obj.oid,
            name=name,
            description=raw_obj.desc or getattr(mux_element, 'description', None),
            qualifier=raw_obj.qual,
            ref_id=raw_obj.dest,
            must=raw_obj.must,
            ref_textmap=getattr(mux_element, 'ref_textmap', None),
            cases=getattr(mux_element, 'cases', ()),
            structure=getattr(mux_element, 'structure', None),
            bit_length=getattr(mux_element, 'bit_length', 0),
            display_format=getattr(mux_element, 'display_format', None),
            encoding=getattr(mux_element, 'encoding', None),
            byte_order=getattr(mux_element, 'byte_order', None),
        )
