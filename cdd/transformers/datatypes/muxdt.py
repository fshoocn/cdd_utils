"""Muxdt → MultiplexedElement 转换器"""
from typing import Any, Optional, List

from ..base import BaseTransformer
from ...compat import Muxdt, Case, Name, Tuv
from ...models.containers import MultiplexedElement, MuxCase, StructElement
from ...registry import ObjectRegistry


class MuxdtTransformer(BaseTransformer):
    """将 Muxdt（多路复用数据类型）转换为 MultiplexedElement"""

    priority = 50
    handles_type = Muxdt

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Muxdt)

    def transform(self, raw_obj: Muxdt, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> MultiplexedElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed Multiplexed Data"),
                 Tuv(lang="zh-CN", value="未命名多路复用数据")]
        )

        # 递归确保选择器引用的数据类型已转换
        ref_textmap = self._resolve_one(
            raw_obj.dtref, registry, warnings, strict,
            context=f"MUXDT {raw_obj.id} ",
        ) if raw_obj.dtref else None

        from ..transformer_registry import TransformerRegistry
        tr = TransformerRegistry()

        # 解析默认结构
        default_structure = None
        if raw_obj.structure:
            default_structure = tr.transform_one(raw_obj.structure, registry, warnings, strict)

        # 解析分支
        cases = []
        if raw_obj.case:
            for raw_case in raw_obj.case:
                mux_case = self._parse_case(raw_case, tr, registry, warnings, strict)
                if mux_case:
                    cases.append(mux_case)

        return MultiplexedElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            ref_textmap=ref_textmap,
            structure=default_structure,
            cases=tuple(cases),
        )

    def _parse_case(self, raw_case: Case, tr, registry: ObjectRegistry,
                    warnings: list, strict: bool) -> Optional[MuxCase]:
        if not raw_case.structure:
            return None

        structure_element = tr.transform_one(raw_case.structure, registry, warnings, strict)
        if not structure_element:
            return None

        try:
            s_val = int(raw_case.s) if isinstance(raw_case.s, (int, str)) else 0
            e_val = int(raw_case.e) if isinstance(raw_case.e, (int, str)) else 0
        except (ValueError, TypeError):
            warnings.append(f"无法解析 Case 范围: s={raw_case.s}, e={raw_case.e}")
            s_val = 0
            e_val = 0

        return MuxCase(s=s_val, e=e_val, structure=structure_element)
