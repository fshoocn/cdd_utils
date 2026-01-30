"""
StructdtParser: 解析 STRUCTDT（结构体数据类型）

STRUCTDT 定义了一个结构体数据类型，包含：
- name: 名称
- qual: 限定符
- cvaluetype: 编码值类型
- pvaluetype: 物理值类型
- struct: 内嵌的结构体定义 (Optional)
- dataobj: 内嵌的数据对象 (Optional)

解析为 StructElement。
"""

from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import StructElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ..base_parser import BaseParser
from ..factory import ParserFactory
from ...models.candela import Structdt, Name, Tuv


@logging
class StructdtParser(BaseParser):
    """
    解析 STRUCTDT（结构体数据类型）为 StructElement
    
    STRUCTDT 通常包含一个 STRUCT 或 DATAOBJ 作为其内容定义。
    """
    priority = 50

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Structdt 类型"""
        return isinstance(raw_obj, Structdt)

    def parse(
        self,
        raw_obj: Structdt,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> StructElement:
        """
        解析 Structdt 对象为 StructElement

        Args:
            raw_obj: Structdt 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            StructElement: 解析后的结构体元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Struct Data Type"),
                Tuv(lang="zh-CN", value="结构体数据类型")
            ]
        )

        # 解析 CVALUETYPE 属性
        cval = raw_obj.cvaluetype
        bit_length = cval.bl if cval and cval.bl else 0
        byte_order = ByteOrder(str(cval.bo)) if cval and cval.bo else ByteOrder.BIG_ENDIAN
        encoding = Encoding(cval.enc) if cval and cval.enc else Encoding.UNSIGNED
        display_format = DisplayFormat(cval.df) if cval and cval.df else DisplayFormat.HEX
        quantity = Quantity(cval.qty) if cval and cval.qty else Quantity.ATOM
        sig = cval.sig if cval else None
        minsz = cval.minsz if cval and cval.minsz else 0
        maxsz = cval.maxsz if cval and cval.maxsz else 0

        # 解析内嵌内容 (struct 或 dataobj)
        children = []
        factory = ParserFactory()
        
        # 尝试解析 inner struct
        if raw_obj.struct:
            inner_element = factory.parse(
                raw_obj.struct, 
                raw_data_map, 
                strict=strict, 
                get_data_from_id=get_data_from_id
            )
            if isinstance(inner_element, StructElement):
                 children.extend(inner_element.struct)
            elif inner_element:
                 children.append(inner_element)
                 
        # 尝试解析 inner dataobj
        elif raw_obj.dataobj:
             inner_element = factory.parse(
                raw_obj.dataobj,
                raw_data_map,
                strict=strict,
                get_data_from_id=get_data_from_id
            )
             if inner_element:
                 children.append(inner_element)

        self._logger.debug(
            f"解析 STRUCTDT: id={raw_obj.id}, oid={raw_obj.oid}, "
            f"children_count={len(children)}"
        )

        # 构建 StructElement
        element = StructElement(
            id=raw_obj.oid, # 通常使用 OID 作为引用 ID
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            
            # 编码属性
            bit_length=bit_length,
            byte_order=byte_order,
            encoding=encoding,
            display_format=display_format,
            quantity=quantity,
            sig=sig,
            minsz=minsz,
            maxsz=maxsz,
            
            # 结构内容
            struct=children,
        )

        return element
