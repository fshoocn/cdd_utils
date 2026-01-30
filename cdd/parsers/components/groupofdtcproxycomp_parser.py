"""
GroupofdtcproxycompParser: 解析 GROUPOFDTCPROXYCOMP (DTC组代理组件)

GROUPOFDTCPROXYCOMP 用于代理 DTC 组信息，包含 minbl/maxbl 和 dtref 属性。
"""

from typing import Any, Callable, Dict, Optional

from ..base_parser import BaseParser
from ...models.candela import Groupofdtcproxycomp, Name, Tuv
from ...models.cdd_model import DiagnosticElement, Quantity


class GroupofdtcproxycompParser(BaseParser):
    """解析 GROUPOFDTCPROXYCOMP 元素"""

    priority = 50

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Groupofdtcproxycomp)

    def parse(
        self,
        raw_obj: Groupofdtcproxycomp,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> DiagnosticElement:
        """
        解析 GROUPOFDTCPROXYCOMP 为 DiagnosticElement
        
        Args:
            raw_obj: GROUPOFDTCPROXYCOMP 对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            DiagnosticElement: 解析后的代理元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed GroupOfDtc Proxy"),
                Tuv(lang="zh-CN", value="未命名DTC组代理组件")
            ]
        )
        element = get_data_from_id(raw_obj.dtref)
        element.must = raw_obj.must
        element.id = raw_obj.id
        element.name = name
        element.description = raw_obj.desc
        element.qualifier = raw_obj.qual
        element.spec = raw_obj.dest
        if raw_obj.minbl == raw_obj.maxbl and raw_obj.minbl is not None:
            element.bit_length = raw_obj.minbl
            element.minsz = 1;
            element.maxsz = 1;
            element.quantity =  Quantity.ATOM
        else:
            element.bit_length = 1
            element.minsz = raw_obj.minbl
            element.maxsz = raw_obj.maxbl if raw_obj.maxbl is not None else raw_obj.minbl
            element.quantity =  Quantity.FIELD
        

        return element
