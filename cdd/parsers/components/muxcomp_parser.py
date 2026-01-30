"""
MuxcompParser: 解析 MUXCOMP（多路复用组件）

MUXCOMP 是一个引用类型，指向一个 MUXDT 定义。
它本身包含：
- selref: 选择器引用
- selbm: 选择器位掩码 (Selector Bit Mask)
- dest: 指向 MUXDT 的引用
- name: 名称
- desc: 描述
- qual: 限定符

解析时需要：
1. 获取引用的 MUXDT 对象（通过 dest）
2. 解析 MUXDT 的内容（分支 case 等）
3. 返回 MultiplexedElement，并包含选择器信息
"""

from typing import Any, Callable, Dict, Optional

from ...utils.logging import logging
from ...models.cdd_model import MultiplexedElement, DiagnosticElement
from ..base_parser import BaseParser
from ...models.candela import Muxcomp, Name, Tuv


@logging
class MuxcompParser(BaseParser):
    """
    解析 MUXCOMP（多路复用组件）为 MultiplexedElement
    
    MUXCOMP 引用 MUXDT，通过 dest 属性关联。
    """
    priority = 50

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Muxcomp 类型"""
        return isinstance(raw_obj, Muxcomp)

    def parse(
        self,
        raw_obj: Muxcomp,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> MultiplexedElement:
        """
        解析 Muxcomp 对象为 MultiplexedElement

        Args:
            raw_obj: Muxcomp 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            MultiplexedElement: 解析后的多路复用元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Multiplexed Component"),
                Tuv(lang="zh-CN", value="多路复用组件")
            ]
        )

        # 获取目标 MUXDT
        mux_element: Optional[MultiplexedElement] = None
        if raw_obj.dest:
            try:
                # MUXDT 应该已被 MuxdtParser 解析为 MultiplexedElement
                mux_element = get_data_from_id(raw_obj.dest)
            except Exception as e:
                 self._logger.warning(f"获取 MUXCOMP 目标失败: dest={raw_obj.dest}, error={e}")

        # 如果找不到引用，返回空壳
        if mux_element is None:
             self._logger.warning(f"MUXCOMP 引用目标未找到或类型错误: dest={raw_obj.dest}")
             return MultiplexedElement(
                id=raw_obj.oid,
                name=name,
                description=raw_obj.desc,
                qualifier=raw_obj.qual,
            )

        self._logger.debug(
            f"解析 MUXCOMP: oid={raw_obj.oid}, dest={raw_obj.dest}, "
            f"selref={raw_obj.selref}, selbm={raw_obj.selbm}"
        )

        # 构建 MultiplexedElement (基于 MUXDT 的内容，加上 MUXCOMP 的上下文)
        # 注意：这里我们创建一个新对象，虽然大部分属性从 mux_element 继承/复制
        # 因为 MUXCOMP 可能有自己的特定属性 (如 must)
        
        element = MultiplexedElement(
            id=raw_obj.oid,
            name=name,
            description=raw_obj.desc if raw_obj.desc else mux_element.description,
            qualifier=raw_obj.qual,
            ref_id=raw_obj.dest, # 保留对 MUXDT 的引用
            must=raw_obj.must,   # MUXCOMP 自己的属性
            
            # 从 MUXDT 继承的属性
            ref_textmap=mux_element.ref_textmap,
            cases=mux_element.cases,
            structure=mux_element.structure,
            
            # Selector 信息暂未在 MultiplexedElement 定义相应字段
            # 如果模型支持 select_ref/select_mask，可在此处添加
             display_format=mux_element.display_format,
             encoding=mux_element.encoding,
             byte_order=mux_element.byte_order,
             bit_length=mux_element.bit_length,
        )

        return element
