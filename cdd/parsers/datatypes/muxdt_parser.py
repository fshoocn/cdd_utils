from typing import Any, Callable, Dict, Optional, List

from ...utils.logging import logging
from ...models.cdd_model import MultiplexedElement, MuxCase, StructElement, Name, Tuv
from ..base_parser import BaseParser
from ...models.candela import Muxdt, Case, Structure
from ..factory import ParserFactory


@logging
class MuxdtParser(BaseParser):
    """
    解析 MUXDT (多路复用数据类型) 为 MultiplexedElement。

    MUXDT 根据选择器 (selector/dtref) 的值，决定使用哪个分支结构。
    包含默认分支 (`structure`) 和多个条件分支 (`case`)。
    """
    priority = 50

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Muxdt 类型"""
        return isinstance(raw_obj, Muxdt)

    def parse(
        self,
        raw_obj: Muxdt,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> MultiplexedElement:
        """
        解析 Muxdt 对象

        Args:
            raw_obj: Muxdt 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            MultiplexedElement: 解析后的多路复用元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed Multiplexed Data"),
                Tuv(lang="zh-CN", value="未命名多路复用数据")
            ]
        )

        # 1. 解析 dtref (选择器引用)
        ref_textmap = None
        if raw_obj.dtref:
             # dtref 通常指向 TEXTTBL，作为选择器的文本映射表
             # 从缓存获取已解析的 TextTableElement
            ref_textmap = get_data_from_id(raw_obj.dtref)

        # 2. 准备 Factory 用于解析内部 Structure
        # 因为 Structure 没有 ID，无法通过 get_data_from_id 获取，需要手动调用工厂
        factory = ParserFactory()
        
        # 3. 解析默认结构 (Structure)
        default_structure = None
        if raw_obj.structure:
            default_structure = factory.parse(
                raw_obj.structure,
                raw_data_map,
                strict=strict,
                get_data_from_id=get_data_from_id
            )

        # 4. 解析分支 (Cases)
        cases: List[MuxCase] = []
        if raw_obj.case:
            for raw_case in raw_obj.case:
                mux_case = self._parse_case(
                    raw_case, 
                    factory, 
                    raw_data_map, 
                    strict=strict,
                    get_data_from_id=get_data_from_id
                )
                if mux_case:
                    cases.append(mux_case)

        # 构建 MultiplexedElement
        element = MultiplexedElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            ref_textmap=ref_textmap,
            structure=default_structure,
            cases=cases
        )

        self._logger.debug(
            f"解析 MUXDT: id={raw_obj.id}, "
            f"cases_count={len(cases)}"
        )

        return element

    def _parse_case(
        self,
        raw_case: Case,
        factory: ParserFactory,
        raw_data_map: Dict[str, Any],
        strict,
        get_data_from_id: Callable[[str], Any]
    ) -> Optional[MuxCase]:
        """解析单个 Case 分支"""
        if not raw_case.structure:
            return None
        
        # 解析 Case 内部的 Structure
        structure_element = factory.parse(raw_case.structure, raw_data_map, strict=strict, get_data_from_id=get_data_from_id)
        
        if not structure_element:
            return None

        # 转换 s (start) 和 e (end) 值为 int
        # candela 定义 s/e 为 Union[int, str]，通常是 int 或十进制/十六进制字符串
        try:
            s_val = int(raw_case.s) if isinstance(raw_case.s, (int, str)) else 0
            e_val = int(raw_case.e) if isinstance(raw_case.e, (int, str)) else 0
        except (ValueError, TypeError):
             self._logger.warning(f"无法解析 Case 范围: s={raw_case.s}, e={raw_case.e}")
             s_val = 0
             e_val = 0

        return MuxCase(
            s=s_val,
            e=e_val,
            structure=structure_element
        )

    def _parse_structure(
        self,
        raw_structure: Structure,
        factory: ParserFactory,
        raw_data_map: Dict[str, Any],
        get_data_from_id: Callable[[str], Any]
    ) -> Optional[StructElement]:
        """通过 ParserFactory 解析 Structure"""
        try:
             # Structure 对象可能不在 StructParser 的目标范围
             # 但 Structure 通常会被某个 解析器 处理
             # 查看 Structure 定义，包含 content 字段，类似于 STRUCT。
             # 我们可能需要一个专门解析 Structure 对象的 Parser，或者复用 StructParser。
             # 假设有 StructureParser，则 factory 能找到匹配 Structure 类型的 parser。
             # 如果没有 StructureParser，我们可能需要在这里直接解析，或将其提交到 StructParser。
             
             # 实际上，Structure 和 STRUCT 相似，可能共用 Struct。
             # 检查是否有 StructureParser，如果没有，可能需要实现一个，或在这里直接处理。
             # 我们的用户提到 "使用 ParserFactory 进行解析"，这意味着应该有一个能处理 Structure 的 parser。
             # 所以我们假设 factory.parse 能处理 Structure 对象
             
             result = factory.parse(raw_structure, raw_data_map, get_data_from_id)
             if isinstance(result, StructElement):
                 return result
             else:
                 self._logger.warning(f"解析 Structure 返回了非 StructElement 类型: {type(result)}")
                 return None
                 
        except Exception as e:
            self._logger.error(f"解析 Structure 失败: {e}")
            return None
