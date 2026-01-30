from typing import Any, Callable, Dict, List, Optional

from ...utils.logging import logging
from ...models.cdd_model import StructElement, DiagnosticElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ..base_parser import BaseParser
from ...models.candela import Contentcomp, Name, Tuv, Specdataobj, Dataobj, Godtcdataobj, Struct, Recorddataobj, Diddataref, Gapdataobj


@logging
class ContentcompParser(BaseParser):
    """
    解析 CONTENTCOMP（内容组件）为 StructElement
    
    CONTENTCOMP 是一个容器组件，包含 SIMPLECOMPCONT（简单内容），它
    本身可以包含多个数据对象（DATAOBJ, SPECDATAOBJ, STRUCT 等），
    通常用于复杂响应的层次结构。
    """
    priority = 50  # 中等优先级

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Contentcomp 类型"""
        return isinstance(raw_obj, Contentcomp)

    def parse(
        self,
        raw_obj: Contentcomp,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> StructElement:
        """
        解析 Contentcomp 对象为 StructElement

        Args:
            raw_obj: Contentcomp 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            ContentElement: 解析后的内容元素
        """
        # 获取名称，若无则使用默认名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed Content Component"),
                Tuv(lang="zh-CN", value="未命名内容组件")
            ]
        )

        # 确定子元素列表
        children: List[DiagnosticElement] = []
        
        if raw_obj.simplecompcont:
            scc = raw_obj.simplecompcont
            
            # 使用 items 字段遍历元素，保持原始顺序
            for item in scc.items:
                id = item.id if item.id is not None else item.oid
                element = get_data_from_id(id)  # 这里可能传入没有ID的情况（有些元素没有ID，此时使用oid），在Cdd_Parser中创建raw_map的时候已经处理了这个逻辑，请放心
                children.append(element)


        self._logger.debug(
            f"解析 CONTENTCOMP: id={raw_obj.id}, "
            f"items_count={len(raw_obj.simplecompcont.items) if raw_obj.simplecompcont else 0}"
        )
        # 构建 ContentElement
        element = StructElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            must=raw_obj.must if raw_obj.must is not None else 1,
            
            min_num_of_items=1,
            max_num_of_items=1,
            struct=children,
        )

        return element
