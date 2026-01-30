from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import DiagnosticElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ..base_parser import BaseParser
from ...models.candela import Ident, Name, Tuv


@logging
class IdentParser(BaseParser):
    """
    解析 IDENT（标识符/数据类型）为 DiagnosticElement。
    
    IDENT 用于描述数据的基础属性，如长度、编码、字节序等。
    通常被 DATAOBJ 等组件引用。
    """
    priority = 50

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Ident 类型"""
        return isinstance(raw_obj, Ident)

    def parse(
        self,
        raw_obj: Ident,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> DiagnosticElement:
        """
        解析 Ident 对象为 DiagnosticElement

        Args:
            raw_obj: Ident 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            DiagnosticElement: 解析后的基础属性元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed Ident"),
                Tuv(lang="zh-CN", value="未命名Ident数据类型")
            ]
        )

        self._logger.debug(
            f"解析 IDENT: id={raw_obj.id}, "
            f"bit_length={raw_obj.cvaluetype.bl}, "
            f"encoding={raw_obj.cvaluetype.enc}"
        )
        # 构建 DiagnosticElement
        element = DiagnosticElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,

            bit_length=raw_obj.cvaluetype.bl,
            display_format=raw_obj.pvaluetype.df,
            encoding=raw_obj.cvaluetype.enc,
            byte_order=ByteOrder(str(raw_obj.cvaluetype.bo).lower()),
            sig=raw_obj.cvaluetype.sig,
            quantity=raw_obj.cvaluetype.qty,
            minsz=raw_obj.cvaluetype.minsz,
            maxsz=raw_obj.cvaluetype.maxsz,
            excl=raw_obj.excl,
        )

        return element
