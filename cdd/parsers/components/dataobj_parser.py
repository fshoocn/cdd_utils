from typing import Any, Callable, Dict, Optional
import copy

from ...utils.logging import logging
from ..base_parser import BaseParser
from ...models.candela import Dataobj
from ...models.cdd_model import DiagnosticElement, Name, Tuv


@logging
class DataobjParser(BaseParser):
    """
    解析 DATAOBJ (数据对象)。
    
    DATAOBJ 通常作为一个实例存在，它们引用一个数据类型对象 (通过 dtref)。
    它可以覆盖特定的名称、描述和标识符。
    """
    priority = 60

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Dataobj 类型"""
        return isinstance(raw_obj, Dataobj)

    def parse(
        self,
        raw_obj: Dataobj,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> DiagnosticElement:
        """
        解析 Dataobj 对象

        Args:
            raw_obj: Dataobj 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            DiagnosticElement: 解析后的元素（基于引用的数据类型）
        """
        # 1. 获取引用的数据类型对象
        # 注意：这里获取的是共享的数据类型对象，必须复制一份，否则修改属性会影响其他引用该类型的地方
        element = get_data_from_id(raw_obj.dtref)
        
        if element is None:
            # 在严格模式下get_data_from_id 会抛出异常，否则返回 None
            if strict:
                raise ValueError(f"DATAOBJ {raw_obj.id or raw_obj.oid} 引用了无效的 dtref: {raw_obj.dtref}")
            else:
                 # 返回一个空占位符（或返回未定义）
                 # 由调用方处理
                 return None

        # 3. 覆盖属性
        # 覆盖名称
        if raw_obj.name:
            element.name = raw_obj.name
            
        # 覆盖限定符
        if raw_obj.qual:
            element.qualifier = raw_obj.qual
            
        # 覆盖描述
        if raw_obj.desc:
            element.description = raw_obj.desc

        # 覆盖 ID
        # 优先 DATAOBJ 的 ID，使用它。否则使用 oid
        # 确保最终生成的 element 有唯一的实例 ID，而不是数据类型的 ID
        if raw_obj.id:
            element.id = raw_obj.id
        elif raw_obj.oid:
            element.id = raw_obj.oid
        
        element.constvalue = raw_obj.v 
        
        # 覆盖 spec
        if raw_obj.spec:
            element.spec = raw_obj.spec
            
        self._logger.debug(
            f"解析 DATAOBJ: oid={raw_obj.oid}, name={element.name.tuv[0].value if element.name and element.name.tuv else 'N/A'}"
        )

        return element
