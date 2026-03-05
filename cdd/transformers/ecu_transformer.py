"""Ecu → EcuModel 转换器"""
from typing import Any

from .base import BaseTransformer
from ..compat import Ecu, Name, Tuv
from ..models.ecu import EcuModel
from ..registry import ObjectRegistry


class EcuTransformer(BaseTransformer):
    """将 Ecu 转换为 EcuModel"""

    priority = 90
    handles_type = Ecu

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Ecu)

    def transform(self, raw_obj: Ecu, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> EcuModel:
        name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed ECU"),
                 Tuv(lang="zh-CN", value="未命名 ECU")]
        )

        # 递归确保所有 DiagClass 已转换
        diag_list = self._resolve_children(
            raw_obj.var.diag, registry, warnings, strict,
            context="ECU ",
        )

        return EcuModel(
            id=raw_obj.id,
            name=name,
            qualifier=raw_obj.qual,
            diag_list=tuple(diag_list),
        )
