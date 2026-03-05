"""Groupofdtcproxycomp → CodedElement 转换器"""
from typing import Any

from ..base import BaseTransformer
from ...compat import Groupofdtcproxycomp, Name, Tuv
from ...models.base import CodedElement, Quantity
from ...registry import ObjectRegistry
import dataclasses


class GroupofdtcproxycompTransformer(BaseTransformer):
    """将 Groupofdtcproxycomp（DTC组代理组件）转换为 CodedElement"""

    priority = 50
    handles_type = Groupofdtcproxycomp

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Groupofdtcproxycomp)

    def transform(self, raw_obj: Groupofdtcproxycomp, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> CodedElement:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed GroupOfDtc Proxy"),
                 Tuv(lang="zh-CN", value="未命名DTC组代理组件")]
        )

        # 递归确保引用的数据类型已转换
        ref_element = self._resolve_one(
            raw_obj.dtref, registry, warnings, strict,
            context=f"GROUPOFDTCPROXYCOMP {raw_obj.id} ",
        )
        if ref_element is None:
            warnings.append(f"GROUPOFDTCPROXYCOMP {raw_obj.id} 引用了无效的 dtref: {raw_obj.dtref}")
            return CodedElement(id=raw_obj.id, name=name)

        if raw_obj.minbl == raw_obj.maxbl and raw_obj.minbl is not None:
            bit_length = raw_obj.minbl
            minsz = 1
            maxsz = 1
            quantity = Quantity.ATOM
        else:
            bit_length = 1
            minsz = raw_obj.minbl
            maxsz = raw_obj.maxbl if raw_obj.maxbl is not None else raw_obj.minbl
            quantity = Quantity.FIELD

        # 用 dataclasses.replace 覆盖属性
        overrides = {
            'id': raw_obj.id,
            'name': name,
            'description': raw_obj.desc,
            'qualifier': raw_obj.qual,
            'spec': raw_obj.dest,
            'must': raw_obj.must,
            'bit_length': bit_length,
            'minsz': minsz,
            'maxsz': maxsz,
            'quantity': quantity,
        }
        try:
            element = dataclasses.replace(ref_element, **overrides)
        except (TypeError, Exception):
            element = CodedElement(
                id=raw_obj.id, name=name, description=raw_obj.desc,
                qualifier=raw_obj.qual, spec=raw_obj.dest, must=raw_obj.must,
                bit_length=bit_length, minsz=minsz, maxsz=maxsz, quantity=quantity,
            )

        return element
