"""
RecorddataobjParser: 解析 RECORDDATAOBJ（记录数据对象）

RECORDDATAOBJ 是一个包含 RECORDDT 的数据对象，用于 DTC 故障快照等场景。
它包含自己的 name、qual、rtSpec，以及内嵌的 RECORDDT。

解析时获取 RECORDDT 的解析结果（TextTableElement），
并用自身的 NAME、QUAL 等属性覆盖。
"""

from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import TextTableElement
from ..base_parser import BaseParser
from ..factory import ParserFactory
from ...models.candela import Recorddataobj, Name, Tuv


@logging
class RecorddataobjParser(BaseParser):
    """
    解析 RECORDDATAOBJ（记录数据对象）为 TextTableElement
    
    获取内嵌 RECORDDT 的解析结果，并用自身的元数据覆盖。
    """
    priority = 55  # 略高于 RecorddtParser

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Recorddataobj 类型"""
        return isinstance(raw_obj, Recorddataobj)

    def parse(
        self,
        raw_obj: Recorddataobj,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> TextTableElement:
        """
        解析 Recorddataobj 对象为 TextTableElement

        Args:
            raw_obj: Recorddataobj 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            TextTableElement: 解析后的文本映射元素
        """
        # 获取 RECORDDATAOBJ 自身的名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Record Data Object"),
                Tuv(lang="zh-CN", value="记录数据对象")
            ]
        )

        # 检查内嵌的 RECORDDT
        if raw_obj.recorddt is None:
            self._logger.warning(f"RECORDDATAOBJ 缺少 RECORDDT: oid={raw_obj.oid}")
            return TextTableElement(
                id=raw_obj.oid,
                name=name,
                description=raw_obj.desc,
                qualifier=raw_obj.qual,
                spec=raw_obj.rt_spec,
                textmap=[],
            )

        # 解析内嵌的 RECORDDT
        factory = ParserFactory()
        recorddt_element: TextTableElement = factory.parse(
            raw_obj.recorddt, 
            raw_data_map, 
            strict=strict, 
            get_data_from_id=get_data_from_id
        )

        self._logger.debug(
            f"解析 RECORDDATAOBJ: oid={raw_obj.oid}, rtSpec={raw_obj.rt_spec}, "
            f"textmap_count={len(recorddt_element.textmap)}"
        )

        # 用 RECORDDATAOBJ 自身的元数据覆盖 RECORDDT 的
        element = TextTableElement(
            id=raw_obj.oid,
            name=name,
            description=raw_obj.desc if raw_obj.desc else recorddt_element.description,
            qualifier=raw_obj.qual,
            spec=raw_obj.rt_spec,
            
            # 从 RECORDDT 继承编码属性
            bit_length=recorddt_element.bit_length,
            byte_order=recorddt_element.byte_order,
            encoding=recorddt_element.encoding,
            display_format=recorddt_element.display_format,
            quantity=recorddt_element.quantity,
            sig=recorddt_element.sig,
            minsz=recorddt_element.minsz,
            maxsz=recorddt_element.maxsz,
            
            # 从 RECORDDT 继承 textmap
            textmap=recorddt_element.textmap,
        )

        return element
