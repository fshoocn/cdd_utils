from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import TextTableElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ..base_parser import BaseParser
from ...models.candela import Staticcomp, Name, Tuv, Texttbl


@logging
class StaticcompParser(BaseParser):
    """
    解析 STATICCOMP（静态组件）为 StaticElement。
    
    STATICCOMP 与 CONSTCOMP 不同，它不直接包含固定值，而是通过 dtref 引用一个
    数据类型对象（通常是 TEXTTBL），该数据类型对象定义了可能的取值范围和对应的文本描述。
    
    spec 常见值:
        - 'sid': 服务标识符 (Service ID)
        - 'sub': 子功能码 (Subfunction)，只有此类型支持响应抑制位 (respsupbit)
        - 'id': 标识符
        - 'accm': 访问模式
        - 'no': 无特殊语义
    """
    priority = 50  # 中等优先级

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Staticcomp 类型"""
        return isinstance(raw_obj, Staticcomp)

    def parse(
        self,
        raw_obj: Staticcomp,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> TextTableElement:
        """
        解析 Staticcomp 对象为 TextTableElement

        Args:
            raw_obj: Staticcomp 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            TextTableElement: 解析后的静态元素
        """
        # 获取名称，若无则使用默认名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed Static Component"),
                Tuv(lang="zh-CN", value="未命名静态组件")
            ]
        )

        # 响应抑制位 (respsupbit) 只在 spec='sub'（子功能码）时有效
        response_suppress_bit = None
        if raw_obj.spec == 'sub' and raw_obj.respsupbit is not None:
            response_suppress_bit = raw_obj.respsupbit
        element : TextTableElement = get_data_from_id(raw_obj.dtref)
        element.id = raw_obj.id
        element.name = name
        # element.ref_id = raw_obj.dtref
        element.must = raw_obj.must if raw_obj.must is not None else 0
        element.response_suppress_bit = response_suppress_bit

        self._logger.debug(
            f"解析 TEXTTABLEELEMENT: id={raw_obj.id}, "
            f"spec={raw_obj.spec}, dtref={raw_obj.dtref}"
            + (f", respsupbit={response_suppress_bit}" if response_suppress_bit else "")
        )

        return element
