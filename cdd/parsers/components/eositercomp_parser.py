"""
EosItercompParser: 解析 EOSITERCOMP (结束标记迭代器组件)

EOSITERCOMP 用于描述可重复的数据块结构，比如 DTC 列表中的每个 DTC 项。
迭代器通过 minNumOfItems 和 maxNumOfItems 定义重复次数的范围。
"""

from typing import Any, Callable, Dict, List, Optional

from ..base_parser import BaseParser
from ...models.candela import Eositercomp, Name, Tuv
from ...models.cdd_model import StructElement, DiagnosticElement
from ..factory import ParserFactory


class EositercompParser(BaseParser):
    """解析 EOSITERCOMP 元素"""

    priority = 50

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Eositercomp)

    def parse(
        self,
        raw_obj: Eositercomp,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> StructElement:
        """
        解析 EOSITERCOMP 为 StructElement
        
        Args:
            raw_obj: EOSITERCOMP 对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取解析后数据的回调函数

        Returns:
            StructElement: 解析后的结束标记迭代器元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed EosIter Component"),
                Tuv(lang="zh-CN", value="未命名迭代器组件")
            ]
        )

        # 解析子组件 - 使用 items 字段保持原始顺序
        children: List[DiagnosticElement] = []

        # EOSITERCOMP 的 items 字段保持了 XML 中的原始顺序
        for comp in raw_obj.items:
            id = comp.id if comp.id is not None else comp.oid
            children.append(get_data_from_id(id))

        return StructElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            must=raw_obj.must,
            min_num_of_items=raw_obj.min_num_of_items if raw_obj.min_num_of_items is not None else 0,
            max_num_of_items=raw_obj.max_num_of_items,
            struct=children,
        )

