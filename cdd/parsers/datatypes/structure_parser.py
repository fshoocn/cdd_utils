"""
StructureParser: 解析 STRUCTURE 和 STRUCT 类型

STRUCTURE 是纯容器类型，只包含 items 列表。
STRUCT 是结构体引用，包含完整的元数据（oid, name, desc, qual, spec, dtref）和 items 列表。

两者都解析为 StructElement。
"""

from typing import Any, Callable, Dict, Optional, List, Union

from ...utils.logging import logging
from ...models.cdd_model import StructElement, DiagnosticElement
from ..base_parser import BaseParser
from ...models.candela import Structure, Struct, Name, Tuv
from ..factory import ParserFactory


@logging
class StructureParser(BaseParser):
    """
    解析 STRUCTURE 和 STRUCT 类型为 StructElement。
    
    - STRUCTURE: 纯容器，只有 items 列表
    - STRUCT: 结构体引用，有完整元数据和 items 列表
    """
    priority = 50
    
    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Structure 或 Struct 类型"""
        return isinstance(raw_obj, (Structure, Struct))

    def parse(
        self, 
        raw_obj: Union[Structure, Struct], 
        raw_data_map: Dict[str, Any], 
        strict: bool = True, 
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> StructElement:
        """
        解析 Structure 或 Struct 对象为 StructElement
        """
        # 解析子元素
        children: List[DiagnosticElement] = []
        
        if raw_obj.items:
            for item in raw_obj.items:
                # 获取 item 的 ID
                item_id = getattr(item, 'id', None) or getattr(item, 'oid', None)
                if item_id:
                    try:
                        element = get_data_from_id(item_id)
                        if element:
                            children.append(element)
                            self._logger.debug(f"解析子元素: id={item_id}")
                    except Exception as e:
                        self._logger.warning(f"解析子元素失败: id={item_id}, error={e}")
                        if strict:
                            raise

        # 根据类型构建 StructElement
        if isinstance(raw_obj, Struct):
            # STRUCT: 使用完整的元数据
            name = raw_obj.name if raw_obj.name is not None else Name(
                tuv=[
                    Tuv(lang="en-US", value="Unnamed Struct"),
                    Tuv(lang="zh-CN", value="未命名结构体")
                ]
            )
            
            self._logger.debug(
                f"解析 STRUCT: oid={raw_obj.oid}, spec={raw_obj.spec}, "
                f"dtref={raw_obj.dtref}, children_count={len(children)}"
            )
            
            element = StructElement(
                id=raw_obj.oid,
                name=name,
                description=raw_obj.desc,
                qualifier=raw_obj.qual,
                spec=raw_obj.spec,
                ref_id=raw_obj.dtref,
                struct=children,
            )
        else:
            # STRUCTURE: 纯容器，使用默认名称
            self._logger.debug(f"解析 STRUCTURE: children_count={len(children)}")
            
            element = StructElement(
                name=Name(
                    tuv=[
                        Tuv(lang="en-US", value="Structure"),
                        Tuv(lang="zh-CN", value="结构体")
                    ]
                ),
                struct=children
            )
        
        return element
