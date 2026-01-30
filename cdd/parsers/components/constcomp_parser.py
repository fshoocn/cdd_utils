from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import ByteOrder, DiagnosticElement, DisplayFormat, Encoding, Quantity
from ..base_parser import BaseParser
from ...models.candela import Constcomp, Name, Tuv


@logging
class ConstcompParser(BaseParser):
    """
    解析 CONSTCOMP（常量组件）为 DiagnosticElement。
    
    CONSTCOMP 用于表示固定值的数据，如 SID、子功能码等。
    
    spec 常见值:
        - 'sid': 服务标识符 (Service ID)
        - 'sub': 子功能码 (Subfunction)，只有此类型支持响应抑制位 (respsupbit)
        - 'no': 无特殊语义
    """
    priority = 50  # 中等优先级

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Constcomp 类型"""
        return isinstance(raw_obj, Constcomp)

    def parse(
        self,
        raw_obj: Constcomp,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> DiagnosticElement:
        """
        解析 Constcomp 对象为 DiagnosticElement

        Args:
            raw_obj: Constcomp 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            DiagnosticElement: 解析后的常量元素
        """
        # 获取名称，若无则使用默认名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed Const Component"),
                Tuv(lang="zh-CN", value="未命名常量组件")
            ]
        )

        # 响应抑制位 (respsupbit) 只在 spec='sub'（子功能码）时有效
        # 根据 UDS 协议特性，只有子功能码可以设置响应抑制位
        response_suppress_bit = None
        if raw_obj.spec == 'sub' and raw_obj.respsupbit is not None:
            response_suppress_bit = raw_obj.respsupbit


        self._logger.debug(
            f"解析 CONSTCOMP: id={raw_obj.id}, "
            f"spec={raw_obj.spec}, bl={raw_obj.bl}, v={raw_obj.v}"
            + (f", respsupbit={response_suppress_bit}" if response_suppress_bit else "")
        )
        # 构建 DiagnosticElement
        element = DiagnosticElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec=raw_obj.spec,                          # 规范类型，如 'sid', 'sub' 等
            bit_length=raw_obj.bl if raw_obj.bl is not None else 8,  # 位长度
            constvalue=raw_obj.v if raw_obj.v is not None else 0,         # 常量值
            must=raw_obj.must if raw_obj.must is not None else 1,    # 是否必须
            response_suppress_bit=response_suppress_bit,             # 响应抑制位（仅 sub 有效）

            # 常量通常使用默认编码属性
            display_format=DisplayFormat.HEX,
            encoding=Encoding.UNSIGNED,
            byte_order=ByteOrder.BIG_ENDIAN,
            quantity=Quantity.ATOM,
        )

        return element
