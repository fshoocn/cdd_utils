"""
GapdataobjParser: 解析 GAPDATAOBJ（占位数据对象）

GAPDATAOBJ 是一个占位数据类型，用于填充信号中的保留位或未使用位。
常见于 19 服务 DTC 故障状态信息中。

主要属性:
    - oid: 对象标识符
    - bl: 位长度 (bit length)
    - name: 名称
    - desc: 描述
    - qual: 限定符
"""

from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import PlaceholderElement
from ..base_parser import BaseParser
from ...models.candela import Gapdataobj, Name, Tuv


@logging
class GapdataobjParser(BaseParser):
    """
    解析 GAPDATAOBJ（占位数据对象）为 PlaceholderElement
    
    GAPDATAOBJ 用于表示保留位或未使用位的占位符。
    """
    priority = 50

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Gapdataobj 类型"""
        return isinstance(raw_obj, Gapdataobj)

    def parse(
        self,
        raw_obj: Gapdataobj,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> PlaceholderElement:
        """
        解析 Gapdataobj 对象为 PlaceholderElement

        Args:
            raw_obj: Gapdataobj 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            PlaceholderElement: 解析后的占位元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Gap Data"),
                Tuv(lang="zh-CN", value="占位数据")
            ]
        )

        # 获取位长度
        bit_length = raw_obj.bl if raw_obj.bl is not None else 0

        self._logger.debug(
            f"解析 GAPDATAOBJ: oid={raw_obj.oid}, bl={bit_length}"
        )

        # 构建 PlaceholderElement
        # 注意: PlaceholderElement 的 description 有默认值，仅在有值时覆盖
        element = PlaceholderElement(
            id=raw_obj.oid,
            name=name,
            qualifier=raw_obj.qual,
            bit_length=bit_length,
        )
        
        # 仅在有描述时覆盖默认值
        if raw_obj.desc is not None:
            element.description = raw_obj.desc

        return element
