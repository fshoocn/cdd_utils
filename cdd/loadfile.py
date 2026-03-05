"""CDD 文件加载入口

提供 load_cdd() 函数作为 V2 解析器的唯一入口。

Example:
    >>> from Backend.cdd_v2 import load_cdd
    >>> db = load_cdd("ECU_ABC.cdd")
    >>> db.services[0]
    >>> db.services.ReadDTCInformation
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Union

from xsdata.formats.dataclass.parsers import XmlParser

from .compat import Candela
from .database import CddDatabase

logger = logging.getLogger(__name__)


def load_cdd(
    path: Union[str, Path],
    *,
    strict: bool = True,
) -> CddDatabase:
    """加载 CDD 文件并返回可查询的 Database 对象

    Args:
        path: CDD 文件路径
        strict: 严格模式（True=错误即停，False=容错并收集警告）

    Returns:
        CddDatabase: 完整的、可查询的诊断数据库

    Raises:
        FileNotFoundError: CDD 文件不存在
        Exception: 解析过程中遇到的错误（仅 strict=True 时）

    Example:
        >>> db = load_cdd("ECU_ABC.cdd")
        >>> service = db.services.ReadDTCInformation
        >>> print(service.qualifier)
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CDD 文件不存在: {path}")

    logger.info(f"[V2] 开始加载 CDD 文件: {path}")

    # Phase 0: XML → Candela (xsdata)
    candela = XmlParser().from_path(path, Candela)
    logger.info(f"[V2] Phase 0 完成: XML 解绑定 (dtdvers={candela.dtdvers})")

    # Phase 1-4: Candela → CddDatabase
    db = CddDatabase(candela, strict=strict)
    logger.info(f"[V2] 加载完成: {db}")

    return db


def load_cdd_from_candela(
    candela: Candela,
    *,
    strict: bool = True,
) -> CddDatabase:
    """从已有的 Candela 对象构建 CddDatabase

    适用于已经通过 xsdata 解析了 XML 的场景。

    Args:
        candela: xsdata 解析后的 Candela 对象
        strict: 严格模式

    Returns:
        CddDatabase: 完整的、可查询的诊断数据库
    """
    return CddDatabase(candela, strict=strict)
