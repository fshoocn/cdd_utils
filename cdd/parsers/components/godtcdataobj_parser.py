"""
GodtcdataobjParser: 解析 GODTCDATAOBJ（DTC 组数据对象）

GODTCDATAOBJ (Group of DTC Data Object) 是一个 DTC 故障码组数据对象，
包含一个内嵌的 TEXTTBL，用于定义 DTC 值到文本的映射。

主要属性:
    - oid: 对象标识符
    - spec: 规格说明（如 'gdtc' 表示 Group DTC）
    - individual_dtcs: 独立 DTC 标志
    - name: 名称
    - desc: 描述
    - qual: 限定符
    - texttbl: 内嵌的文本映射表
"""

from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import TextTableElement
from ..base_parser import BaseParser
from ..factory import ParserFactory
from ...models.candela import Godtcdataobj, Name, Tuv


@logging
class GodtcdataobjParser(BaseParser):
    """
    解析 GODTCDATAOBJ（DTC 组数据对象）为 TextTableElement
    
    获取内嵌 TEXTTBL 的解析结果，并用自身的元数据覆盖。
    """
    priority = 55

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Godtcdataobj 类型"""
        return isinstance(raw_obj, Godtcdataobj)

    def parse(
        self,
        raw_obj: Godtcdataobj,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> TextTableElement:
        """
        解析 Godtcdataobj 对象为 TextTableElement

        Args:
            raw_obj: Godtcdataobj 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            TextTableElement: 解析后的文本映射元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Group of DTC Data Object"),
                Tuv(lang="zh-CN", value="DTC 组数据对象")
            ]
        )

        # 检查内嵌的 TEXTTBL
        if raw_obj.texttbl is None:
            self._logger.warning(f"GODTCDATAOBJ 缺少 TEXTTBL: oid={raw_obj.oid}")
            return TextTableElement(
                id=raw_obj.oid,
                name=name,
                description=raw_obj.desc,
                qualifier=raw_obj.qual,
                spec=raw_obj.spec,
                textmap=[],
            )

        # 解析内嵌的 TEXTTBL
        factory = ParserFactory()
        texttbl_element: TextTableElement = factory.parse(
            raw_obj.texttbl, 
            raw_data_map, 
            strict=strict, 
            get_data_from_id=get_data_from_id
        )

        self._logger.debug(
            f"解析 GODTCDATAOBJ: oid={raw_obj.oid}, spec={raw_obj.spec}, "
            f"individualDtcs={raw_obj.individual_dtcs}, textmap_count={len(texttbl_element.textmap)}"
        )

        # 用 GODTCDATAOBJ 自身的元数据覆盖
        element = TextTableElement(
            id=raw_obj.oid,
            name=name,
            description=raw_obj.desc if raw_obj.desc else texttbl_element.description,
            qualifier=raw_obj.qual,
            spec=raw_obj.spec,
            
            # 从 TEXTTBL 继承编码属性
            bit_length=texttbl_element.bit_length,
            byte_order=texttbl_element.byte_order,
            encoding=texttbl_element.encoding,
            display_format=texttbl_element.display_format,
            quantity=texttbl_element.quantity,
            sig=texttbl_element.sig,
            minsz=texttbl_element.minsz,
            maxsz=texttbl_element.maxsz,
            
            # 从 TEXTTBL 继承 textmap
            textmap=texttbl_element.textmap,
        )

        return element
