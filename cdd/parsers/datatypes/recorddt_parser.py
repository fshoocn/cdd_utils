"""
RecorddtParser: 解析 RECORDDT（记录数据类型）

RECORDDT 是一个 DTC 记录数据类型定义，包含：
- name: 名称
- qual: 限定符
- cvaluetype: 编码值类型（bit length, byte order, encoding 等）
- pvaluetype: 物理值类型
- record: RECORD 列表，每个 RECORD 包含一个 DTC 值 (v) 和文本描述 (text)

解析为 TextTableElement，每个 RECORD 对应一个 Textmap。
"""

from typing import Any, Callable, Dict, List, Optional

from ...utils.logging import logging
from ...models.cdd_model import (
    TextTableElement, ByteOrder, DisplayFormat, Encoding, Quantity
)
from ..base_parser import BaseParser
from ...models.candela import Recorddt, Textmap, Name, Tuv


@logging
class RecorddtParser(BaseParser):
    """
    解析 RECORDDT（记录数据类型）为 TextTableElement
    
    每个 RECORD 的 v 值和 text 转换为 Textmap。
    """
    priority = 50

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Recorddt 类型"""
        return isinstance(raw_obj, Recorddt)

    def parse(
        self,
        raw_obj: Recorddt,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> TextTableElement:
        """
        解析 Recorddt 对象为 TextTableElement

        Args:
            raw_obj: Recorddt 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            TextTableElement: 解析后的文本映射元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Record Data Type"),
                Tuv(lang="zh-CN", value="记录数据类型")
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
        maxsz = cval.maxsz if cval and cval.maxsz else 255

        # 解析 RECORD 列表为 Textmap
        textmap_list: List[Textmap] = []
        
        for record in raw_obj.record:
            # record.v 是 DTC 值（如 9651456 = 0x935700）
            # record.text 是描述文本
            v = record.v if record.v is not None else 0
            
            # 获取文本内容
            text_content = None
            if record.text and record.text.tuv:
                text_content = record.text
            
            # 创建 Textmap，s 和 e 都为 v（单值映射）
            textmap = Textmap(s=v, e=v, text=text_content)
            textmap_list.append(textmap)
            
            self._logger.debug(f"解析 RECORD: v=0x{v:06X}, text={text_content}")

        self._logger.debug(
            f"解析 RECORDDT: id={raw_obj.id}, oid={raw_obj.oid}, "
            f"record_count={len(textmap_list)}"
        )

        # 构建 TextTableElement
        element = TextTableElement(
            id=raw_obj.oid,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            bit_length=bit_length,
            byte_order=byte_order,
            encoding=encoding,
            display_format=display_format,
            quantity=quantity,
            sig=sig,
            minsz=minsz,
            maxsz=maxsz,
            textmap=textmap_list,
        )

        return element
