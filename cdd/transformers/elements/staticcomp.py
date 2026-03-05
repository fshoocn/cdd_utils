"""Staticcomp → TextTableElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Staticcomp, Name, Tuv
from ...models.elements import TextTableElement
from ...registry import ObjectRegistry
import dataclasses


class StaticcompTransformer(BaseTransformer):
    """将 Staticcomp（静态组件）转换为 TextTableElement
    
    STATICCOMP 通过 dtref 引用一个数据类型对象（通常是 TEXTTBL），
    用自身属性覆盖后返回。
    """

    priority = 50
    handles_type = Staticcomp

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Staticcomp)

    def transform(self, raw_obj: Staticcomp, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> TextTableElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed Static Component"),
                 Tuv(lang="zh-CN", value="未命名静态组件")]
        )

        response_suppress_bit = None
        if raw_obj.spec == 'sub' and raw_obj.respsupbit is not None:
            response_suppress_bit = raw_obj.respsupbit

        # 递归确保引用的数据类型已转换
        ref_element = self._resolve_one(
            raw_obj.dtref, registry, warnings, strict,
            context=f"STATICCOMP {raw_obj.id} ",
        )
        if ref_element is None:
            warnings.append(f"STATICCOMP {raw_obj.id} 引用了无效的 dtref: {raw_obj.dtref}")
            return TextTableElement(
                id=raw_obj.id,
                name=name,
                must=raw_obj.must if raw_obj.must is not None else 0,
            )

        # 用 dataclasses.replace 覆盖属性
        overrides = {
            'id': raw_obj.id,
            'name': name,
            'must': raw_obj.must if raw_obj.must is not None else 0,
            'response_suppress_bit': response_suppress_bit,
        }

        try:
            element = dataclasses.replace(ref_element, **overrides)
        except (TypeError, Exception):
            # 如果引用元素不是同类型 dataclass，构建一个新的
            element = TextTableElement(
                id=raw_obj.id,
                name=name,
                must=raw_obj.must if raw_obj.must is not None else 0,
                response_suppress_bit=response_suppress_bit,
            )

        return element
