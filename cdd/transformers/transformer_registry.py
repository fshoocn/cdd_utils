"""转换器注册表 — 替代现有 ParserFactory

自动发现并管理所有转换器，提供按类型快速匹配。
核心方法 transform_one() 是整个转换流程的单一入口点：
- 幂等：已转换的对象直接返回
- 递归：转换器内部可安全地嵌套调用 transform_one
- 防环：_transforming set 检测循环引用（每次 build 隔离）
- 自注册：转换结果自动写入 registry
"""
import importlib
import inspect
import logging
import pkgutil
from collections import defaultdict
from pathlib import Path
from typing import Any, Optional, List

from .base import BaseTransformer
from ..registry import ObjectRegistry
from ..utils.exceptions import TransformError

logger = logging.getLogger(__name__)


class TransformerRegistry:
    """自动发现并管理所有转换器

    特性：
    - 自动发现 transformers/ 目录下所有 BaseTransformer 子类
    - 按 handles_type 建立快速索引（O(1) 查找 vs 线性扫描）
    - 按 priority 排序，优先级高的先匹配
    - transform_one 支持：幂等 + 循环检测 + 自动注册
    - _transforming 状态隔离到每次构建，不跨实例污染
    """
    _instance = None
    _transformers: Optional[List[BaseTransformer]] = None
    _type_index: Optional[dict] = None    # {type → [transformer]}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if TransformerRegistry._transformers is None:
            TransformerRegistry._transformers = []
            self._discover_transformers()
            self._build_type_index()
        self.transformers = TransformerRegistry._transformers
        # 循环引用检测：每次 reset_state() 创建新 set，隔离不同 build
        if not hasattr(self, '_transforming'):
            self._transforming: set[str] = set()

    def reset_state(self):
        """重置转换状态（每次 Phase 2 开始时调用）"""
        self._transforming = set()

    def _discover_transformers(self):
        """自动发现所有转换器"""
        transformer_path = Path(__file__).parent
        # 动态确定包前缀：使用本模块的包名
        package_prefix = __name__.rsplit('.', 1)[0]  # e.g. "Backend.cdd_v2.transformers"
        logger.debug(f"扫描转换器目录: {transformer_path} (prefix={package_prefix})")
        self._scan_package(transformer_path, package_prefix)
        TransformerRegistry._transformers.sort(key=lambda t: t.priority, reverse=True)
        logger.info(
            f"[V2] 已加载转换器: {[t.__class__.__name__ for t in TransformerRegistry._transformers]}"
        )

    def _scan_package(self, package_path: Path, package_prefix: str):
        """递归扫描包中的转换器"""
        for _, name, is_pkg in pkgutil.iter_modules([str(package_path)]):
            full_module_name = f"{package_prefix}.{name}"
            if is_pkg:
                sub_path = package_path / name
                self._scan_package(sub_path, full_module_name)
            else:
                try:
                    module = importlib.import_module(full_module_name)
                    for _, obj in inspect.getmembers(module, inspect.isclass):
                        if (issubclass(obj, BaseTransformer)
                                and obj is not BaseTransformer
                                and not getattr(obj, '__abstractmethods__', set())):
                            TransformerRegistry._transformers.append(obj())
                            logger.debug(f"加载转换器: {obj.__name__}")
                except Exception as e:
                    logger.warning(f"加载转换器模块失败: {full_module_name}. 错误: {e}")

    def _build_type_index(self):
        """构建 {type → [transformer]} 快速索引"""
        index: dict[type, list[BaseTransformer]] = defaultdict(list)
        for t in TransformerRegistry._transformers:
            if t.handles_type is not None:
                index[t.handles_type].append(t)
        TransformerRegistry._type_index = dict(index)
        logger.debug(f"类型索引: {len(TransformerRegistry._type_index)} 个类型已索引")

    def find_transformer(self, raw_obj: Any) -> Optional[BaseTransformer]:
        """按类型查找匹配的转换器

        优先通过 handles_type 索引 O(1) 查找，
        未命中再 fallback 到线性扫描（兼容 match 方法覆盖多类型的场景）。
        """
        obj_type = type(raw_obj)
        # 快速路径：精确类型索引
        if TransformerRegistry._type_index:
            candidates = TransformerRegistry._type_index.get(obj_type)
            if candidates:
                for t in candidates:
                    if t.match(raw_obj):
                        return t
        # 慢速路径：线性扫描（处理 isinstance 多类型匹配等场景）
        for transformer in self.transformers:
            if transformer.match(raw_obj):
                return transformer
        return None

    def transform_one(
        self,
        raw_obj: Any,
        registry: ObjectRegistry,
        warnings: list,
        strict: bool = True,
    ) -> Any:
        """转换单个对象（核心入口点）

        特性：
        1. 幂等：已转换的对象直接返回缓存结果
        2. 循环检测：防止 A→B→A 无限递归
        3. 自动注册：转换结果自动写入 registry.model_objects
        4. 递归安全：转换器内部可嵌套调用本方法

        Args:
            raw_obj: 原始 Candela 对象
            registry: 对象注册表
            warnings: 警告收集列表
            strict: 是否严格模式

        Returns:
            转换后的 CDD 模型对象，无转换器或失败时返回 None
        """
        obj_id = getattr(raw_obj, 'id', None) or getattr(raw_obj, 'oid', None)

        # ① 幂等：已转换则直接返回
        if obj_id and registry.has_model(obj_id):
            return registry.get_model(obj_id)

        # ② 循环检测
        if obj_id and obj_id in self._transforming:
            logger.debug(f"循环引用检测，跳过: {obj_id} ({type(raw_obj).__name__})")
            return None

        # ③ 查找转换器（无转换器 → 静默返回 None）
        transformer = self.find_transformer(raw_obj)
        if transformer is None:
            return None

        # ④ 标记「正在转换」→ 执行转换 → 自动注册
        if obj_id:
            self._transforming.add(obj_id)

        try:
            model = transformer.transform(raw_obj, registry, warnings, strict)

            # 自动注册（防止重复注册）
            if model is not None and obj_id and not registry.has_model(obj_id):
                registry.register_transformed(obj_id, model)

            return model

        except Exception as e:
            obj_id_str = obj_id or 'unknown'
            if strict:
                raise TransformError(
                    transformer.__class__.__name__, obj_id_str, e
                ) from e
            msg = f"转换器 {transformer.__class__.__name__} 处理 {obj_id_str} 失败: {e}"
            warnings.append(msg)
            logger.warning(msg)
            return None

        finally:
            if obj_id:
                self._transforming.discard(obj_id)


class TransformerNotFoundError(Exception):
    pass
