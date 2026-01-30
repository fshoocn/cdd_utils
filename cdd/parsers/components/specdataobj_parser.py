"""
SpecdataobjParser: 解析 SPECDATAOBJ (特殊数据对象)

SPECDATAOBJ 是一种特殊的数据对象，通常用于定义负响应码（NRC）列表。
它包含一组 NEGRESCODEPROXY 引用，指向预定义的负响应码定义（NEGRESCODE）。

解析逻辑：
    - 将整个 NEGRESCODEPROXIES 解析为一个 TextTableElement
    - 将每个 NEGRESCODEPROXY 引用的 NEGRESCODE 解析为一个 Textmap
    - Textmap.s = Textmap.e = NEGRESCODE.v（负响应码值）
    - Textmap.text = NEGRESCODE.name（负响应码名称）

主要属性:
    - oid: 对象标识符
    - name: 名称
    - qual: 限定符
    - negrescodeproxies: 负响应码代理列表
"""

from typing import Any, Callable, Dict, List, Optional

from ...utils.logging import logging
from ...models.cdd_model import TextTableElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ..base_parser import BaseParser
from ...models.candela import Specdataobj, Name, Tuv, Textmap, Text, Negrescode


@logging
class SpecdataobjParser(BaseParser):
    """
    解析 SPECDATAOBJ（特殊数据对象）为 TextTableElement
    
    SPECDATAOBJ 通常用于定义服务可能返回的负响应码列表。
    通过 NEGRESCODEPROXY 引用 NEGRESCODE，最终解析为包含 Textmap 的 TextTableElement。
    """
    priority = 55  # 中等优先级

    def match(self, raw_obj: Any) -> bool:
        """判断是否为 Specdataobj 类型"""
        return isinstance(raw_obj, Specdataobj)

    def parse(
        self,
        raw_obj: Specdataobj,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> TextTableElement:
        """
        解析 Specdataobj 对象为 TextTableElement

        Args:
            raw_obj: Specdataobj 原始对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            TextTableElement: 解析后的文本映射元素，包含所有负响应码
        """
        # 获取名称，若无则使用默认名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Negative Response Codes"),
                Tuv(lang="zh-CN", value="负响应码列表")
            ]
        )

        # 解析 NEGRESCODEPROXIES -> Textmap 列表
        textmap_list: List[Textmap] = []
        
        if raw_obj.negrescodeproxies and raw_obj.negrescodeproxies.negrescodeproxy:
            for proxy in raw_obj.negrescodeproxies.negrescodeproxy:
                if proxy.idref:
                    # 从 raw_data_map 中获取引用的 NEGRESCODE 对象
                    negrescode: Negrescode = raw_data_map.get(proxy.idref)
                    
                    if negrescode is None:
                        self._logger.warning(f"找不到 NEGRESCODE 引用: {proxy.idref}")
                        continue
                    
                    # 将 NEGRESCODE 转换为 Textmap
                    # s = e = v（负响应码值），text = name（负响应码名称）
                    textmap = Textmap(
                        s=negrescode.v,
                        e=negrescode.v,
                        text=Text(tuv=negrescode.name.tuv) if negrescode.name else None,
                        addinfo=None
                    )
                    textmap_list.append(textmap)
                    
                    self._logger.debug(
                        f"解析 NEGRESCODE: id={negrescode.id}, v={negrescode.v}, "
                        f"name={negrescode.name.tuv[0].value if negrescode.name and negrescode.name.tuv else 'N/A'}"
                    )

        self._logger.debug(
            f"解析 SPECDATAOBJ: oid={raw_obj.oid}, "
            f"name={name.tuv[0].value if name.tuv else 'N/A'}, "
            f"nrc_count={len(textmap_list)}"
        )

        # 构建 TextTableElement
        element = TextTableElement(
            id=raw_obj.oid,  # SPECDATAOBJ 只有 oid
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec="nrc",  # 标记为负响应码类型
            
            # NRC 通常是 1 字节
            bit_length=8,
            display_format=DisplayFormat.HEX,
            encoding=Encoding.UNSIGNED,
            byte_order=ByteOrder.BIG_ENDIAN,
            quantity=Quantity.ATOM,
            
            # 文本映射列表
            textmap=textmap_list,
        )

        return element
