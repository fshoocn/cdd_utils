"""
DiddatarefParser: 解析 DIDDATAREF 和 DIDREF (DID 数据引用)

DIDDATAREF 和 DIDREF 都是引用类型，通过 didRef 属性引用 DID（Data Identifier）对象。
DID 对象包含完整的数据结构定义（STRUCTURE），解析时需要：
1. 获取引用的 DID 对象
2. 解析 DID 中的 STRUCTURE 结构
3. 返回包含 DID 编号和数据结构的 DidElement

主要属性:
    - oid: 对象标识符
    - didRef: 引用的 DID 对象 ID
    - name: 名称（可覆盖 DID 的名称）
    - qual: 限定符
"""

from typing import Any, Callable, Dict, List, Optional, Union

from ...utils.logging import logging
from ...models.cdd_model import DidElement, DiagnosticElement
from ..base_parser import BaseParser
from ...models.candela import Diddataref, Didref, Did, Name, Tuv


@logging
class DiddatarefParser(BaseParser):
    """
    解析 DIDDATAREF 和 DIDREF（DID 数据引用）为 DidElement
    
    DIDDATAREF/DIDREF 引用一个 DID 定义，DID 包含：
    - n: DID 编号（如 0xF190）
    - structure: 数据结构，包含多个数据对象
    
    解析后返回 DidElement，其中：
    - did 存储 DID 编号
    - struct 包含解析后的数据结构
    """
    priority = 55  # 中等优先级

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Diddataref 或 Didref 类型"""
        return isinstance(raw_obj, (Diddataref, Didref))

    def parse(
        self,
        raw_obj: Union[Diddataref, Didref],
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> DidElement:
        """
        解析 Diddataref/Didref 对象为 DidElement

        Args:
            raw_obj: Diddataref 或 Didref 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            DidElement: 解析后的 DID 元素，包含 DID 编号和数据结构
        """
        # 获取名称，优先使用 raw_obj 自身的名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed DID Data Reference"),
                Tuv(lang="zh-CN", value="未命名 DID 数据引用")
            ]
        )

        # 获取引用的 DID 对象
        did: Did = raw_data_map.get(raw_obj.did_ref)
        
        # 安全获取描述（Didref 没有 desc 属性）
        desc = getattr(raw_obj, 'desc', None)

        if did is None:
            self._logger.warning(f"找不到 DID 引用: {raw_obj.did_ref}")
            return DidElement(
                id=raw_obj.oid,
                name=name,
                description=desc,
                qualifier=raw_obj.qual,
                did=0,
                struct=[],
            )

        # 使用 DID 的名称（如果引用对象没有指定）
        if raw_obj.name is None and did.name is not None:
            name = did.name

        # 使用 DID 的描述（如果引用对象没有指定）
        if desc is None:
            desc = did.desc

        # 解析 DID 的 STRUCTURE 中的数据对象
        children: List[DiagnosticElement] = []
        
        if did.structure and did.structure.items:
            for item in did.structure.items:
                item_id = getattr(item, 'id', None) or getattr(item, 'oid', None)
                if item_id:
                    try:
                        element: DiagnosticElement = get_data_from_id(item_id)
                        if element:
                            children.append(element)
                            self._logger.debug(f"解析 DID 数据元素: id={item_id}")
                    except Exception as e:
                        self._logger.warning(f"解析 DID 数据元素失败: id={item_id}, error={e}")
                        if strict:
                            raise

        # DID 编号（如 0xF190 = 61840）
        did_number = did.n if did.n is not None else 0

        self._logger.debug(
            f"解析 DIDREF/DIDDATAREF: oid={raw_obj.oid}, didRef={raw_obj.did_ref}, "
            f"DID=0x{did_number:04X}, children_count={len(children)}"
        )

        # 构建 DidElement
        element = DidElement(
            id=raw_obj.oid,
            name=name,
            description=desc,
            qualifier=raw_obj.qual,
            did=did_number,
            struct=children,
        )

        return element
