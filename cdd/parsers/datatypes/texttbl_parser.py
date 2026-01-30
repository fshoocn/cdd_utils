from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import TextTableElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ..base_parser import BaseParser
from ...models.candela import Texttbl, Name, Tuv


@logging
class TexttblParser(BaseParser):
    """
    解析 TEXTTBL（文本表）为 TextTableElement。

    TEXTTBL 用于建立数据值与文本值之间的映射关系，
    通常在 STATICCOMP 中通过 dtref 属性引用，实现数据的可视化显示。

    主要属性:
        - CVALUETYPE: 常量值类型，定义数据的物理属性和编码方式
        - PVALUETYPE: 物理值类型，定义显示格式
        - TEXTMAP: 文本映射，通过 s(start) 和 e(end) 的范围建立映射
    """
    priority = 50

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Texttbl 类型"""
        return isinstance(raw_obj, Texttbl)

    def parse(
        self,
        raw_obj: Texttbl,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> TextTableElement:
        """
        解析 Texttbl 对象为 TextTableElement

        Args:
            raw_obj: Texttbl 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            TextTableElement: 解析后的文本表元素
        """
        # 获取名称，若无则使用默认名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed Text Table"),
                Tuv(lang="zh-CN", value="未命名文本表")
            ]
        )

        bit_length = raw_obj.cvaluetype.bl
        display_format = raw_obj.pvaluetype.df
        encoding = raw_obj.cvaluetype.enc
        byte_order = ByteOrder(str(raw_obj.cvaluetype.bo).lower())
        sig = raw_obj.cvaluetype.sig
        quantity = raw_obj.cvaluetype.qty
        minsz = raw_obj.cvaluetype.minsz
        maxsz = raw_obj.cvaluetype.maxsz


        # 获取文本映射列表
        textmap = raw_obj.textmap

        # 排除某些范围的数据值
        excl = raw_obj.excl

        # 构建 TextTableElement
        element = TextTableElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            bit_length=bit_length,
            display_format=display_format,
            encoding=encoding,
            sig=sig,
            byte_order=byte_order,
            quantity=quantity,
            minsz=minsz,
            maxsz=maxsz,
            excl=excl,
            textmap=textmap,
        )

        self._logger.debug(
            f"解析 TEXTTBL: id={raw_obj.id}, "
            f"bit_length={bit_length}, "
            f"textmap_count={len(raw_obj.textmap) if raw_obj.textmap else 0}"
        )

        return element
