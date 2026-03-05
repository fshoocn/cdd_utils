"""命名项列表 — 支持按名称属性访问的 list

类似 odxtools 的 NamedItemList，支持按 qualifier 属性访问列表中的元素。

Example:
    >>> services = NamedItemList(service_list, lambda s: s.qualifier)
    >>> svc = services.ReadDTCInformation  # 按 qualifier 属性访问
    >>> svc = services[0]                   # 按索引访问
    >>> svc = services.by_name("ReadDTCInformation")  # 按名精确查找
"""
from __future__ import annotations

import re
from typing import TypeVar, Generic, Optional, Iterator, Callable, List

T = TypeVar('T')


class NamedItemList(list, Generic[T]):
    """支持按 qualifier 属性访问的列表
    
    继承自 list，保留所有列表功能（索引、切片、迭代），
    同时支持按名称属性访问。
    
    特性：
    - `list[idx]` 按索引访问
    - `list.QualifierName` 按 qualifier 属性访问
    - `list.by_name(name)` 精确查找
    - `list.search(keyword)` 模糊搜索
    - 名称冲突时属性访问返回第一个匹配项
    """

    def __init__(self, items: List[T] = None, name_getter: Callable[[T], Optional[str]] = None):
        """
        Args:
            items: 初始元素列表
            name_getter: 从元素中提取名称的函数，默认取 qualifier 属性
        """
        super().__init__(items or [])
        self._name_getter = name_getter or (lambda x: getattr(x, 'qualifier', None))
        self._name_index: dict[str, T] = {}
        self._rebuild_index()

    def _rebuild_index(self):
        """重建名称索引"""
        self._name_index.clear()
        for item in self:
            name = self._name_getter(item)
            if name and name not in self._name_index:
                self._name_index[name] = item

    def _safe_name(self, name: str) -> str:
        """将名称转换为合法的 Python 标识符"""
        return re.sub(r'[^a-zA-Z0-9_]', '_', name)

    def __getattr__(self, name: str) -> T:
        """按名称属性访问"""
        if name.startswith('_'):
            raise AttributeError(name)
        # 先精确匹配
        if name in self._name_index:
            return self._name_index[name]
        # 再尝试安全名称匹配
        for key, item in self._name_index.items():
            if self._safe_name(key) == name:
                return item
        raise AttributeError(f"NamedItemList 中没有名为 {name!r} 的元素")

    def by_name(self, name: str) -> Optional[T]:
        """按名称精确查找
        
        Args:
            name: 要查找的名称

        Returns:
            匹配的元素，未找到返回 None
        """
        return self._name_index.get(name)

    def search(self, keyword: str) -> List[T]:
        """按关键词模糊搜索（大小写不敏感）
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            匹配的元素列表
        """
        keyword_lower = keyword.lower()
        return [
            item for item in self
            if keyword_lower in (self._name_getter(item) or '').lower()
        ]

    @property
    def names(self) -> list[str]:
        """所有可用的名称列表"""
        return list(self._name_index.keys())

    def append(self, item: T) -> None:
        super().append(item)
        name = self._name_getter(item)
        if name and name not in self._name_index:
            self._name_index[name] = item

    def extend(self, items) -> None:
        super().extend(items)
        self._rebuild_index()

    def __repr__(self):
        return f"NamedItemList({list.__repr__(self)})"

    def __dir__(self):
        """支持 IDE 自动补全"""
        base = set(super().__dir__())
        # 添加安全名称作为属性
        for name in self._name_index:
            base.add(self._safe_name(name))
        return sorted(base)
