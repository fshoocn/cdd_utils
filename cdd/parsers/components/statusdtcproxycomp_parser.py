from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import DiagnosticElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ..base_parser import BaseParser
from ...models.candela import Statusdtcproxycomp, Name, Tuv


@logging
class StatusdtcproxycompParser(BaseParser):
    """
    解析 STATUSDTCPROXYCOMP（DTC状态代理组件）为 DiagnosticElement
    
    STATUSDTCPROXYCOMP 是专门用于 DTC 状态信息的代理组件，
    通常用于 19 服务（Read DTC Information）的响应中。
    
    dest 常见值:
        - 'dtcStatus': DTC 状态字段
    """
    priority = 50  # 中等优先级

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Statusdtcproxycomp 类型"""
        return isinstance(raw_obj, Statusdtcproxycomp)

    def parse(
        self,
        raw_obj: Statusdtcproxycomp,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> DiagnosticElement:
        """
        解析 Statusdtcproxycomp 对象为 DiagnosticElement

        Args:
            raw_obj: Statusdtcproxycomp 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            DiagnosticElement: 解析后的代理元素
        """
        # 获取名称，若无则使用默认名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed Status DTC Proxy Component"),
                Tuv(lang="zh-CN", value="未命名DTC状态代理组件")
            ]
        )

        self._logger.debug(
            f"解析 STATUSDTCPROXYCOMP: id={raw_obj.id}, "
            f"dest={raw_obj.dest}, minbl={raw_obj.minbl}, maxbl={raw_obj.maxbl}"
        )

        # 构建 DiagnosticElement
        element = DiagnosticElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec= raw_obj.dest,
            must=raw_obj.must,
            
            # 默认属性
            display_format=DisplayFormat.HEX,
            encoding=Encoding.UNSIGNED,
            byte_order=ByteOrder.BIG_ENDIAN,
        )
        if raw_obj.minbl == raw_obj.maxbl and raw_obj.minbl is not None:
            element.bit_length = raw_obj.minbl
            element.minsz = 1
            element.maxsz = 1
            element.quantity =  Quantity.ATOM
        else:
            element.bit_length = 1
            element.minsz = raw_obj.minbl
            element.maxsz = raw_obj.maxbl if raw_obj.maxbl is not None else raw_obj.minbl
            element.quantity =  Quantity.FIELD

        return element

