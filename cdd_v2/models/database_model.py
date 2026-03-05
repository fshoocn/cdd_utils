"""CDD 顶层数据模型"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

from .ecu import EcuModel, StateGroup


@dataclass(frozen=True)
class CddModel:
    """CDD 顶层数据聚合
    
    所有解析后的数据都汇聚于此。
    """
    dtdvers: Optional[str] = None
    state_groups: tuple = ()
    ecu: Optional[EcuModel] = None
