"""转换器基类 — 所有转换器的 ABC

设计原则（参考 odxtools 分阶段架构）：
- transform() 可递归调用 _resolve_children / _resolve_one
  → 依赖对象会被深度优先地按需转换并自动注册
- TransformerRegistry.transform_one() 保证幂等 + 防环 + 自注册
  → 子类无需手动管理注册逻辑
"""
from abc import ABC, abstractmethod
from typing import Any, Type, Optional, List

from ..registry import ObjectRegistry


class BaseTransformer(ABC):
    """将 Candela 原始对象转换为 CDD 模型对象

    职责：
    1. 判断是否能处理某种 Candela 类型（match）
    2. 执行转换：Candela 对象 → CDD 模型对象（transform）
    3. 通过 _resolve_children / _resolve_one 递归解析依赖
    """

    # 优先级：数值越大越优先
    priority: int = 0

    # 声明此转换器处理的 Candela 类型（可选，用于快速索引）
    handles_type: Optional[Type] = None

    @abstractmethod
    def match(self, raw_obj: Any) -> bool:
        """判断是否能处理此对象"""
        ...

    @abstractmethod
    def transform(
        self,
        raw_obj: Any,
        registry: ObjectRegistry,
        warnings: list,
        strict: bool = True,
    ) -> Any:
        """将 Candela 原始对象转换为 CDD 模型对象

        可在内部调用 _resolve_children / _resolve_one 递归解析依赖。
        转换结果由 TransformerRegistry.transform_one() 自动注册，
        子类无需调用 registry.register_transformed()。
        """
        ...

    # ─────── 递归解析辅助方法（供子类使用） ───────

    def _resolve_children(
        self,
        items,
        registry: ObjectRegistry,
        warnings: list,
        strict: bool,
        context: str = "",
    ) -> List[Any]:
        """递归解析一组内联子元素。

        对每个子元素调用 transform_one()，实现深度优先递归转换。
        transform_one 保证幂等（已转换则直接返回）和防环。

        适用场景：
        - Structure/Simplecompcont/Contentcomp 等容器内的 items
        - Req/Pos/Neg 消息内的 items
        - Ecu 的 diag 列表

        Args:
            items: 原始子元素列表（raw Candela objects）
            registry: 对象注册表
            warnings: 警告收集
            strict: 严格模式
            context: 日志上下文（如 "Structure "）

        Returns:
            成功转换的子模型对象列表
        """
        from .transformer_registry import TransformerRegistry
        tr = TransformerRegistry()
        children = []
        if not items:
            return children

        for item in items:
            # transform_one 已处理：幂等检查 → 循环检测 → 转换 → 自动注册
            model = tr.transform_one(item, registry, warnings, strict)
            if model is not None:
                children.append(model)
            else:
                item_id = getattr(item, 'id', None) or getattr(item, 'oid', None)
                if item_id:
                    # 有 ID 却转换失败 → 记录警告
                    msg = f"{context}子元素 {item_id} ({type(item).__name__}) 未能转换"
                    warnings.append(msg)

        return children

    def _resolve_one(
        self,
        ref_id: Optional[str],
        registry: ObjectRegistry,
        warnings: list,
        strict: bool,
        context: str = "",
    ) -> Any:
        """按 ID 递归解析单个引用对象。

        先查已转换模型 → 再取原始对象触发递归转换。
        transform_one 保证幂等和防环。

        适用场景：
        - Dataobj.dtref → 数据类型
        - Muxcomp.dest → Muxdt
        - Muxdt.dtref → 选择器文本映射
        - DiagInst 中 service/shproxy 的引用

        Args:
            ref_id: 引用目标的 ID
            registry: 对象注册表
            warnings: 警告收集
            strict: 严格模式
            context: 日志上下文

        Returns:
            已转换的模型对象，找不到或失败时返回 None
        """
        if not ref_id:
            return None

        # 快速路径：已转换
        model = registry.get_model(ref_id)
        if model is not None:
            return model

        # 取原始对象并递归转换
        raw = registry.get_raw(ref_id)
        if raw is None:
            msg = f"{context}引用目标 {ref_id} 不在注册表中"
            if strict:
                raise ValueError(msg)
            warnings.append(msg)
            return None

        from .transformer_registry import TransformerRegistry
        tr = TransformerRegistry()
        # transform_one 内部会自动注册结果
        return tr.transform_one(raw, registry, warnings, strict)
