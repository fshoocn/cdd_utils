"""
LincompParser: 解析 LINCOMP (线性转换组件)

LINCOMP 用于描述需要进行线性转换的数据元素。
它定义了原始值（CVALUETYPE）到物理值（PVALUETYPE）的转换关系，
转换公式: 物理值 = 原始值 * f + o

主要属性:
    - id: 元素唯一标识
    - bm: 位掩码
    - cvaluetype: 原始值类型（编码值的位长、编码方式等）
    - pvaluetype: 物理值类型（物理值的位长、单位等）
    - comp: 线性转换参数（f=因子, o=偏移量, s=起始值, e=结束值）
    - excl: 排除值列表
"""

from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import LinCompElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ..base_parser import BaseParser
from ...models.candela import Lincomp, Name, Tuv


@logging
class LincompParser(BaseParser):
    """
    解析 LINCOMP（线性转换组件）为 LinCompElement
    
    LINCOMP 定义了原始值到物理值的线性转换关系，
    常用于传感器数据、电压、温度等需要单位转换的场景。
    
    转换公式: 物理值 = 原始值 * (f / div) + o
    其中 div 默认为 1。
    """
    priority = 50  # 中等优先级

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Lincomp 类型"""
        return isinstance(raw_obj, Lincomp)

    def parse(
        self,
        raw_obj: Lincomp,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> LinCompElement:
        """
        解析 Lincomp 对象为 LinCompElement

        Args:
            raw_obj: Lincomp 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            LinCompElement: 解析后的线性转换元素
        """
        # 获取名称，若无则使用默认名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed Linear Component"),
                Tuv(lang="zh-CN", value="未命名线性转换组件")
            ]
        )

        # 解析原始值类型 (CVALUETYPE)
        cvaluetype = raw_obj.cvaluetype
        bit_length = cvaluetype.bl if cvaluetype and cvaluetype.bl is not None else 8
        byte_order = ByteOrder(str(cvaluetype.bo)) if cvaluetype and cvaluetype.bo else ByteOrder.BIG_ENDIAN
        encoding = Encoding(cvaluetype.enc) if cvaluetype and cvaluetype.enc else Encoding.UNSIGNED
        display_format = DisplayFormat(raw_obj.pvaluetype.df) if raw_obj.pvaluetype and raw_obj.pvaluetype.df else DisplayFormat.DECIMAL
        quantity = Quantity(cvaluetype.qty) if cvaluetype and cvaluetype.qty else Quantity.ATOM
        sig = cvaluetype.sig if cvaluetype else None
        minsz = cvaluetype.minsz if cvaluetype and cvaluetype.minsz is not None else 1
        maxsz = cvaluetype.maxsz if cvaluetype and cvaluetype.maxsz is not None else 1

        # 处理排除值列表
        excl_list = list(raw_obj.excl) if raw_obj.excl else []

        self._logger.debug(
            f"解析 LINCOMP: id={raw_obj.id}, name={name.tuv[0].value if name.tuv else 'N/A'}, "
            f"bl={bit_length}, comp.f={raw_obj.comp.f if raw_obj.comp else 'N/A'}, "
            f"comp.o={raw_obj.comp.o if raw_obj.comp else 'N/A'}"
        )

        # 构建 LinCompElement
        element = LinCompElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            
            # 编码属性（来自 CVALUETYPE）
            bit_length=bit_length,
            byte_order=byte_order,
            encoding=encoding,
            display_format=display_format,
            quantity=quantity,
            sig=sig,
            minsz=minsz,
            maxsz=maxsz,
            
            # 排除值
            excl=excl_list,
            
            # 线性转换参数
            comp=raw_obj.comp,
        )

        return element
