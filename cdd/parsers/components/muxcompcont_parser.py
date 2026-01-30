"""
MuxcompcontParser: 解析 MUXCOMPCONT（多路复用组件容器）

MUXCOMPCONT 是一个容器类型，通常用于代理映射场景（包含 shproxyref）。
它可以包含一个内嵌的 MUXDT 或 DATAOBJ。

解析逻辑：
1. 优先解析内嵌的 MUXDT
2. 如果没有 MUXDT，尝试解析 DATAOBJ
3. 返回解析出的 DiagnosticElement (通常是 MultiplexedElement 或 StructElement)
"""

from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import DiagnosticElement
from ..base_parser import BaseParser
from ..factory import ParserFactory
from ...models.candela import Muxcompcont


@logging
class MuxcompcontParser(BaseParser):
    """
    解析 MUXCOMPCONT（多路复用组件容器）
    
    通常包含一个内嵌对象（MUXDT 或 DATAOBJ），通过 ParserFactory 委托解析。
    """
    priority = 50

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Muxcompcont 类型"""
        return isinstance(raw_obj, Muxcompcont)

    def parse(
        self,
        raw_obj: Muxcompcont,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> DiagnosticElement:
        """
        解析 Muxcompcont 对象为 DiagnosticElement

        Args:
            raw_obj: Muxcompcont 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            DiagnosticElement: 解析后的子元素
        """
        factory = ParserFactory()
        element: Optional[DiagnosticElement] = None
        
        # 1. 尝试解析内嵌的 MUXDT
        if raw_obj.muxdt:
            try:
                element = factory.parse(
                    raw_obj.muxdt,
                    raw_data_map,
                    strict=strict,
                    get_data_from_id=get_data_from_id
                )
                self._logger.debug(f"解析 MUXCOMPCONT 内嵌 MUXDT: oid={raw_obj.muxdt.oid}")
            except Exception as e:
                self._logger.warning(f"解析 MUXCOMPCONT 内嵌 MUXDT 失败: {e}")
                if strict:
                     raise

        # 2. 如果没有 MUXDT，尝试解析 DATAOBJ
        elif raw_obj.dataobj:
            try:
                element = factory.parse(
                    raw_obj.dataobj,
                    raw_data_map,
                    strict=strict,
                    get_data_from_id=get_data_from_id
                )
                self._logger.debug(f"解析 MUXCOMPCONT 内嵌 DATAOBJ: oid={raw_obj.dataobj.oid}")
            except Exception as e:
                self._logger.warning(f"解析 MUXCOMPCONT 内嵌 DATAOBJ 失败: {e}")
                if strict:
                    raise

        if element:
            # 记录 MUXCOMPCONT 自身的 OID 和引用信息 (如有需要)
            # 这里我们直接返回解析出的子元素，因为 MUXCOMPCONT 此时充当透明容器
            # 如果需要保留 shproxyref，可能需要修改 element 的属性或包装一层
            if raw_obj.shproxyref:
                 self._logger.debug(f"MUXCOMPCONT 包含 shproxyref: {raw_obj.shproxyref}")
            if raw_obj.oid:
                 self._logger.debug(f"MUXCOMPCONT oid: {raw_obj.oid}")
            
            # 使用 OID 作为 ID（如果子元素没有 ID）
            if not element.id and raw_obj.oid:
                element.id = raw_obj.oid
            
            return element
            
        self._logger.warning(f"MUXCOMPCONT 为空或解析失败: oid={raw_obj.oid}")
        return None  # 或者抛出异常
