"""有类型的延迟引用 — 对标 odxtools OdxLinkRef，但更简洁

在 Phase 2（转换阶段）创建，在 Phase 3（引用解析阶段）被解析为真实对象。
解析后可以透明地当作目标对象使用（代理模式）。
"""
from __future__ import annotations

from typing import TypeVar, Type, Generic, Optional

T = TypeVar('T')


class CddRef(Generic[T]):
    """有类型的延迟引用
    
    在 Phase 2（转换阶段）创建，在 Phase 3（引用解析阶段）被解析为真实对象。
    解析后可以透明地当作目标对象使用。
    
    Example:
        >>> # Phase 2: 转换器创建引用
        >>> ref = registry.create_ref("DT_001", TextTableElement)
        >>> element.data_type = ref
        >>> # Phase 3: 自动解析后
        >>> element.data_type.textmap  # 透明访问真实对象
    """

    __slots__ = ('ref_id', 'expected_type', '_resolved_value', '_is_resolved')

    def __init__(self, ref_id: str, expected_type: Type[T] = object):
        self.ref_id = ref_id
        self.expected_type = expected_type
        self._resolved_value: Optional[T] = None
        self._is_resolved = False

    def _resolve(self, value: T) -> None:
        """内部方法：设置解析后的值（由 ObjectRegistry 调用）"""
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"CddRef({self.ref_id!r}) 期望类型 {self.expected_type.__name__}，"
                f"但实际得到 {type(value).__name__}"
            )
        self._resolved_value = value
        self._is_resolved = True

    @property
    def value(self) -> T:
        """获取解析后的值
        
        Raises:
            RuntimeError: 如果引用尚未解析
        """
        if not self._is_resolved:
            raise RuntimeError(
                f"CddRef({self.ref_id!r}) 尚未解析。"
                f"请确保在 Phase 3 之后访问。"
            )
        return self._resolved_value

    @property
    def is_resolved(self) -> bool:
        return self._is_resolved

    def __getattr__(self, name: str):
        """代理模式：透明转发属性访问到真实对象
        
        当引用已解析时，直接访问底层对象的属性。
        这样使用者不需要知道自己拿到的是引用还是真实对象。
        """
        if name.startswith('_'):
            raise AttributeError(name)
        return getattr(self.value, name)

    def __repr__(self):
        status = "resolved" if self._is_resolved else "pending"
        return f"CddRef({self.ref_id!r}, {self.expected_type.__name__}, {status})"

    def __eq__(self, other):
        if isinstance(other, CddRef):
            return self.ref_id == other.ref_id
        return NotImplemented

    def __hash__(self):
        return hash(self.ref_id)
