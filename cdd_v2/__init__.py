"""CDD 解析器 V2 — 公共 API

基于 4 阶段架构设计：注册 → 转换 → 引用解析 → 冻结

Usage:
    >>> from Backend.cdd_v2 import load_cdd
    >>> db = load_cdd("path/to/file.cdd")
    >>> db.services.ReadDTCInformation
    >>> db.ecu

核心组件:
    - load_cdd: 入口函数
    - CddDatabase: 顶层容器
    - CddRef: 有类型的延迟引用
    - ObjectRegistry: ID 注册表
    - NamedItemList: 按名/按索引访问的列表
"""
from .loadfile import load_cdd, load_cdd_from_candela
from .database import CddDatabase
from .refs import CddRef
from .registry import ObjectRegistry, DuplicateIdError, IdNotFoundError
from .named_list import NamedItemList

__all__ = [
    # 入口函数
    "load_cdd",
    "load_cdd_from_candela",
    # 核心类
    "CddDatabase",
    "CddRef",
    "ObjectRegistry",
    "NamedItemList",
    # 异常
    "DuplicateIdError",
    "IdNotFoundError",
]

__version__ = "2.0.0"
