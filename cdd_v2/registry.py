"""对象注册表 — 管理 ID → 对象的映射，支持分阶段注册和类型安全解析

生命周期：
1. Phase 1 (register): 注册 Candela 原始对象 { id → raw_obj }
2. Phase 2 (register_transformed): 注册转换后的模型对象 { id → model_obj }
3. Phase 3 (resolve): 解析 CddRef[T] → 实际模型对象
"""
from __future__ import annotations

import logging
from typing import Any, TypeVar, Type, Optional, List

from .refs import CddRef

T = TypeVar('T')
logger = logging.getLogger(__name__)


class ObjectRegistry:
    """管理 CDD 对象的全局 ID 注册表
    
    与现有 raw_data / analyzed_data 的区别：
    - 三个阶段，职责清晰
    - get_model() 是纯查询，不触发任何解析
    - resolve() 带类型断言
    - _pending_refs 追踪所有待解析引用
    """

    def __init__(self, *, strict: bool = True):
        self._strict = strict
        # Phase 1: { id → raw Candela object }
        self._raw_objects: dict[str, Any] = {}
        # Phase 2: { id → transformed model object }
        self._model_objects: dict[str, Any] = {}
        # 跟踪所有创建的 CddRef
        self._pending_refs: list[CddRef] = []
        self._transformed_count = 0

    def __len__(self) -> int:
        return len(self._raw_objects)

    @property
    def transformed_count(self) -> int:
        return self._transformed_count

    @property
    def raw_ids(self) -> list[str]:
        """所有已注册的原始对象 ID"""
        return list(self._raw_objects.keys())

    @property
    def model_ids(self) -> list[str]:
        """所有已注册的模型对象 ID"""
        return list(self._model_objects.keys())

    def clear(self):
        """清空所有注册数据"""
        self._raw_objects.clear()
        self._model_objects.clear()
        self._pending_refs.clear()
        self._transformed_count = 0
        # 清除附加缓存（如 DomaindataproxycompTransformer 的 faultmemory 缓存）
        if hasattr(self, '_faultmemory_cache'):
            del self._faultmemory_cache

    # ─── Phase 1: 原始对象注册 ───

    def register(self, obj_id: str, raw_obj: Any) -> None:
        """注册原始对象 ID
        
        Args:
            obj_id: 对象 ID
            raw_obj: 原始 Candela 对象
            
        Raises:
            DuplicateIdError: 严格模式下 ID 重复时抛出
        """
        if obj_id in self._raw_objects:
            if self._strict:
                raise DuplicateIdError(obj_id)
            else:
                logger.warning(f"重复的对象 ID (跳过): {obj_id}")
                return
        self._raw_objects[obj_id] = raw_obj

    def get_raw(self, obj_id: str) -> Any:
        """获取原始对象"""
        return self._raw_objects.get(obj_id)

    def has_raw(self, obj_id: str) -> bool:
        """检查原始对象是否存在"""
        return obj_id in self._raw_objects

    # ─── Phase 2: 模型对象注册 ───

    def register_transformed(self, obj_id: str, model_obj: Any) -> None:
        """注册转换后的模型对象"""
        self._model_objects[obj_id] = model_obj
        self._transformed_count += 1

    def get_model(self, obj_id: str) -> Any:
        """获取模型对象"""
        return self._model_objects.get(obj_id)

    def has_model(self, obj_id: str) -> bool:
        """检查模型对象是否存在"""
        return obj_id in self._model_objects

    # ─── Phase 3: 引用解析 ───

    def create_ref(self, ref_id: str, expected_type: Type[T] = object) -> CddRef[T]:
        """创建一个待解析的引用
        
        在 Phase 2（转换阶段）使用：转换器创建引用而非立即解析。
        
        Args:
            ref_id: 引用目标的 ID
            expected_type: 期望的目标类型（用于 Phase 3 类型检查）
            
        Returns:
            CddRef[T]: 一个待解析的引用
        """
        ref = CddRef(ref_id, expected_type)
        self._pending_refs.append(ref)
        return ref

    def resolve(self, ref_id: str, expected_type: Type[T] = object) -> T:
        """立即解析引用并返回模型对象（用于 Phase 3）
        
        Args:
            ref_id: 引用目标的 ID
            expected_type: 期望的目标类型
            
        Returns:
            目标模型对象
            
        Raises:
            IdNotFoundError: ID 不在注册表中
            TypeError: 实际类型与期望类型不匹配
        """
        obj = self._model_objects.get(ref_id)
        if obj is None:
            if self._strict:
                raise IdNotFoundError(ref_id)
            else:
                logger.warning(f"引用解析失败: {ref_id}")
                return None
        if expected_type is not object and not isinstance(obj, expected_type):
            msg = (
                f"引用 {ref_id} 类型不匹配: "
                f"期望 {expected_type.__name__}，实际 {type(obj).__name__}"
            )
            if self._strict:
                raise TypeError(msg)
            else:
                logger.warning(msg)
        return obj

    def resolve_all_refs(self) -> list[str]:
        """解析所有 Phase 2 中创建的 CddRef，返回未解析的 ID 列表"""
        unresolved = []
        for ref in self._pending_refs:
            if ref.is_resolved:
                continue
            obj = self._model_objects.get(ref.ref_id)
            if obj is not None:
                try:
                    ref._resolve(obj)
                except TypeError as e:
                    if self._strict:
                        raise
                    else:
                        logger.warning(str(e))
                        unresolved.append(ref.ref_id)
            else:
                unresolved.append(ref.ref_id)
                if self._strict:
                    raise IdNotFoundError(ref.ref_id)
                else:
                    logger.warning(f"未找到引用目标: {ref.ref_id}")
        return unresolved


class DuplicateIdError(Exception):
    """重复的对象 ID"""
    def __init__(self, obj_id: str):
        super().__init__(f"重复的对象 ID: {obj_id}")
        self.obj_id = obj_id


class IdNotFoundError(Exception):
    """未找到 ID"""
    def __init__(self, ref_id: str):
        super().__init__(f"未找到 ID: {ref_id}")
        self.ref_id = ref_id
