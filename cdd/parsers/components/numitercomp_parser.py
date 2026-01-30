"""
NumitercompParser: 解析 NUMITERCOMP (数字迭代器组件)

NUMITERCOMP 用于描述通过计数器确定重复次数的数据结构。
selref 引用一个组件（计数器），其值决定迭代次数。
"""

from typing import Any, Callable, Dict, List, Optional

from ..base_parser import BaseParser
from ...models.candela import Numitercomp, Name, Tuv
from ...models.cdd_model import NumIterElement, DiagnosticElement
from ..factory import ParserFactory


class NumitercompParser(BaseParser):
    """解析 NUMITERCOMP 元素"""

    priority = 50

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Numitercomp)

    def parse(
        self,
        raw_obj: Numitercomp,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> NumIterElement:
        """
        解析 NUMITERCOMP 为 NumIterElement
        
        Args:
            raw_obj: NUMITERCOMP 对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取解析后数据的回调函数

        Returns:
            NumIterElement: 解析后的数字迭代器元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed NumIter Component"),
                Tuv(lang="zh-CN", value="未命名数字迭代器组件")
            ]
        )

        # 解析子组件
        children: List[DiagnosticElement] = []
        factory = ParserFactory()

        # NUMITERCOMP 包含一个 SIMPLEPROXYCOMP 子组件
        if raw_obj.simpleproxycomp is not None:
            children.append(factory.parse(raw_obj.simpleproxycomp, raw_data_map, strict=strict, get_data_from_id=get_data_from_id))

        return NumIterElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            must=raw_obj.must if raw_obj.must is not None else 1,
            selref=raw_obj.selref,
            selbm=raw_obj.selbm,
            children=children,
        )
