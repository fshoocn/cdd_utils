"""
DomaindataproxycompParser: 解析 DOMAINDATAPROXYCOMP (域数据代理组件)

DOMAINDATAPROXYCOMP 用于代理某个域中的数据，如记录编号等。
与 SIMPLEPROXYCOMP 相似，但没有 minbl/maxbl 属性，数据长度从引用的数据类型获取。
"""

from typing import Any, Callable, Dict, Optional

from ..base_parser import BaseParser
from ...models.candela import Domaindataproxycomp, Name, Tuv
from ...models.cdd_model import DiagnosticElement


class DomaindataproxycompParser(BaseParser):
    """解析 DOMAINDATAPROXYCOMP 元素"""

    priority = 50

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Domaindataproxycomp)

    def parse(
        self,
        raw_obj: Domaindataproxycomp,
        raw_data_map: Dict[str, Any],
        strict: bool = True,
        get_data_from_id: Optional[Callable[[str], Any]] = None
    ) -> DiagnosticElement:
        """
        解析 DOMAINDATAPROXYCOMP 为 DiagnosticElement
        
        Args:
            raw_obj: DOMAINDATAPROXYCOMP 对象
            raw_data_map: 原始数据映射表
            strict: 是否严格模式
            get_data_from_id: 根据 ID 获取已解析数据的回调函数

        Returns:
            DiagnosticElement: 解析后的代理元素
        """
        # 获取名称
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed DomainData Proxy"),
                Tuv(lang="zh-CN", value="未命名域数据代理组件")
            ]
        )

        return DiagnosticElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec=raw_obj.dest,
            must=raw_obj.must,
            # DOMAINDATAPROXYCOMP 没有 minbl/maxbl，使用默认值
        )
