"""
SimplecompcontParser: 解析 SIMPLECOMPCONT (简单组件内容)

SIMPLECOMPCONT 是一个容器类型，用于包装一组数据对象（DATAOBJ, SPECDATAOBJ, STRUCT 等）。
它通常作为 CONTENTCOMP 或 DIAGINST 的子元素出现，表示一组有序的数据项。

主要属性:
    - oid: 对象标识符
    - temploid: 模板对象标识符
    - shproxyref: 代理引用（用于数据替换）
    - items: 子数据对象列表（DATAOBJ, SPECDATAOBJ, STRUCT, RECORDDATAOBJ 等）
"""

from typing import Any, Callable, Dict, List, Optional, Union

from ...utils.logging import logging
from ...models.cdd_model import StructElement, DiagnosticElement
from ..base_parser import BaseParser
from ...models.candela import Simplecompcont, Name, Tuv


@logging
class SimplecompcontParser(BaseParser):
    """
    解析 SIMPLECOMPCONT（简单组件内容）为 StructElement
    
    SIMPLECOMPCONT 是一个纯容器类型，它本身没有名称、描述等元信息，
    仅包含一组有序的数据对象。解析后转换为 StructElement，
    其中 struct 属性包含所有子元素。
    """
    priority = 55  # 中等优先级，略高于普通组件

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Simplecompcont 类型"""
        return isinstance(raw_obj, Simplecompcont)

    def parse(
        self,
        raw_obj: Simplecompcont,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> Union[DiagnosticElement, StructElement]:
        """
        解析 Simplecompcont 对象为 StructElement

        Args:
            raw_obj: Simplecompcont 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            StructElement: 解析后的结构元素，包含所有子数据对象
        """
        # Simplecompcont 本身没有 name，创建默认名称
        name = Name(
            tuv=[
                Tuv(lang="en-US", value="Simple Component Content"),
                Tuv(lang="zh-CN", value="简单组件内容")
            ]
        )

        # 解析子元素列表
        children: List[DiagnosticElement] = []
        
        for item in raw_obj.items:
            # 获取元素 ID（优先使用 id，其次使用 oid）
            item_id = getattr(item, 'id', None) or getattr(item, 'oid', None)
            
            if item_id:
                try:
                    element: DiagnosticElement = get_data_from_id(item_id)
                    if element:
                        children.append(element)
                        self._logger.debug(f"解析子元素: id={item_id}, type={type(item).__name__}")
                except Exception as e:
                    self._logger.warning(f"解析子元素失败: id={item_id}, error={e}")
                    if strict:
                        raise

        self._logger.debug(
            f"解析 SIMPLECOMPCONT: oid={raw_obj.oid}, "
            f"shproxyref={raw_obj.shproxyref}, "
            f"items_count={len(raw_obj.items)}, "
            f"parsed_count={len(children)}"
        )
        if len(children) == 1:
            return children[0]

        # 构建 StructElement
        element = StructElement(
            id=raw_obj.oid,  # Simplecompcont 只有 oid，没有 id
            name=name,
            description=None,
            qualifier=None,
            spec=raw_obj.shproxyref,  # 使用 shproxyref 作为 spec，用于代理替换匹配
            must=1,  # 默认必须
            
            # 结构属性
            min_num_of_items=1,
            max_num_of_items=1,
            struct=children,
        )

        return element
