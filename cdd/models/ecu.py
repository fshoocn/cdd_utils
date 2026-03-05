"""ECU 模型层 — EcuModel, DiagnosticInstance, DiagnosticGroup"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Union

from .messages import DiagnosticService
from .candela import Name, Desc


@dataclass(frozen=True)
class StateGroup:
    """状态组"""
    name: Name
    qualifier: Optional[str] = None
    spec: str = ""
    state: tuple = ()


@dataclass(frozen=True)
class DiagnosticInstance:
    """诊断实例 — 包含一组诊断服务"""
    name: Name
    id: Optional[str] = None
    description: Optional[Desc] = None
    qualifier: Optional[str] = None
    services: tuple = ()


@dataclass(frozen=True)
class DiagnosticGroup:
    """诊断组 — 包含一组诊断实例"""
    name: Name
    id: Optional[str] = None
    description: Optional[Desc] = None
    qualifier: Optional[str] = None
    diagInst: tuple = ()


@dataclass(frozen=True)
class EcuModel:
    """ECU 模型"""
    id: str
    name: Name
    qualifier: Optional[str] = None
    diag_list: tuple = ()
