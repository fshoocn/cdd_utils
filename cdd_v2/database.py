"""CDD 数据库 — 顶层容器，管理完整的 4 阶段生命周期

Phase 1: 扫描 Candela 对象图，注册所有带 ID 的对象
Phase 2: 将 Candela 原始对象转换为 CDD 模型对象
Phase 3: 解析所有 CddRef[T] 引用
Phase 4: 冻结数据库，构建便捷索引
"""
from __future__ import annotations

import logging
from typing import Optional, Any, List

from .compat import Candela
from .models.database_model import CddModel
from .models.ecu import EcuModel, DiagnosticGroup, DiagnosticInstance
from .models.messages import DiagnosticService, DiagnosticMessage
from .registry import ObjectRegistry
from .named_list import NamedItemList
from .transformers.transformer_registry import TransformerRegistry

logger = logging.getLogger(__name__)


class CddDatabase:
    """CDD 诊断数据库

    管理 CDD 文件的完整生命周期：注册 → 转换 → 引用解析 → 冻结。
    构建完成后是只读的，可安全地在多个线程间共享。

    Attributes:
        model: 解析后的 CDD 数据模型
        ecu: ECU 诊断模型
        services: 所有诊断服务（按 qualifier 可属性访问）
        warnings: 非严格模式下收集的警告列表
    """

    def __init__(self, candela: Candela, *, strict: bool = True):
        self._candela = candela
        self._strict = strict
        self._registry = ObjectRegistry(strict=strict)
        self._transformer_registry = TransformerRegistry()
        self._warnings: list[str] = []
        self._frozen = False

        self._model: Optional[CddModel] = None
        self._services: NamedItemList[DiagnosticService] = NamedItemList()

        # 执行 4 阶段构建
        self.refresh()

    # ──────────────────────── 4 阶段构建 ────────────────────────

    def refresh(self):
        """执行完整的 4 阶段构建流程

        可在修改 Candela 对象后重新调用以刷新数据库。
        """
        self._frozen = False
        self._registry.clear()
        self._warnings.clear()
        self._model = None
        self._services = NamedItemList()

        # Phase 1: 扫描 Candela 对象图，注册所有带 ID 的对象
        self._build_registry()

        # Phase 2: 将 Candela 原始对象转换为 CDD 模型对象
        self._transform()

        # Phase 3: 解析所有 CddRef[T] 引用
        self._resolve_refs()

        # Phase 4: 冻结对象，构建索引
        self._freeze()

    # ─────────────────────────── Phase 1 ───────────────────────────

    def _build_registry(self):
        """Phase 1: 递归扫描 Candela 对象图，注册所有带 id/oid 的对象"""
        self._scan_object(self._candela, seen=set())
        logger.info(f"Phase 1 完成: 注册了 {len(self._registry)} 个对象")

    def _scan_object(self, obj: Any, seen: set):
        """递归遍历对象图并注册 ID"""
        if obj is None:
            return
        obj_identity = id(obj)
        if obj_identity in seen:
            return
        seen.add(obj_identity)

        # 尝试注册（有 id 或 oid 的对象）
        obj_id = getattr(obj, 'id', None)
        if not obj_id:
            obj_id = getattr(obj, 'oid', None)

        if obj_id:
            self._registry.register(obj_id, obj)

        # 递归子对象
        if isinstance(obj, dict):
            for v in obj.values():
                self._scan_object(v, seen)
        elif isinstance(obj, (list, tuple, set)):
            for item in obj:
                self._scan_object(item, seen)
        elif hasattr(obj, '__dict__'):
            for v in obj.__dict__.values():
                self._scan_object(v, seen)
        elif hasattr(obj, '__slots__'):
            for slot in obj.__slots__:
                self._scan_object(getattr(obj, slot, None), seen)

    # ─────────────────────────── Phase 2 ───────────────────────────

    def _transform(self):
        """Phase 2: 递归深度优先转换

        单次遍历所有注册对象。每个转换器内部通过
        _resolve_children / _resolve_one 递归触发依赖的转换，
        TransformerRegistry.transform_one() 保证幂等和防环。

        不需要多 Pass 排序 — 递归自动处理依赖顺序：
        Ecu → Diagclass → Diaginst → Protocolservice → 容器 → 数据类型
        """
        # 重置循环检测状态
        self._transformer_registry.reset_state()

        for obj_id in self._registry.raw_ids:
            if self._registry.has_model(obj_id):
                continue
            raw_obj = self._registry.get_raw(obj_id)
            # transform_one 处理：查找转换器 → 递归转换 → 自动注册
            self._transformer_registry.transform_one(
                raw_obj, self._registry, self._warnings, self._strict
            )

        logger.info(
            f"Phase 2 完成: 转换了 {self._registry.transformed_count} 个对象 "
            f"(共 {len(self._registry)} 个注册对象)"
        )

    def _try_transform(self, obj_id: str, raw_obj: Any):
        """尝试转换单个对象（transform_one 处理递归、注册、防环）"""
        self._transformer_registry.transform_one(
            raw_obj, self._registry, self._warnings, self._strict
        )

    # ─────────────────────────── Phase 3 ───────────────────────────

    def _resolve_refs(self):
        """Phase 3: 遍历所有模型对象，解析 CddRef[T] → 实际对象

        此阶段完成后，所有引用都指向真实对象（共享引用，不拷贝）。
        """
        unresolved = self._registry.resolve_all_refs()
        if unresolved:
            msg = f"有 {len(unresolved)} 个引用无法解析: {unresolved[:10]}"
            if self._strict:
                raise ReferenceError(msg)
            else:
                self._warnings.append(msg)
                logger.warning(msg)
        logger.info("Phase 3 完成: 所有引用已解析")

    # ─────────────────────────── Phase 4 ───────────────────────────

    def _freeze(self):
        """Phase 4: 冻结数据库，构建便捷索引"""
        # 构建 CddModel
        ecu_raw = self._candela.ecudoc.ecu
        ecu_model = self._registry.get_model(ecu_raw.id)

        self._model = CddModel(
            dtdvers=self._candela.dtdvers,
            ecu=ecu_model,
        )

        # 收集所有诊断服务，构建 NamedItemList
        all_services: list[DiagnosticService] = []
        self._collect_services(ecu_model, all_services)
        self._services = NamedItemList(all_services)

        self._frozen = True
        logger.info(
            f"Phase 4 完成: 数据库已冻结，共 {len(self._services)} 个服务"
        )

    def _collect_services(self, obj: Any, result: list):
        """递归收集所有 DiagnosticService"""
        if obj is None:
            return
        if isinstance(obj, DiagnosticService):
            result.append(obj)
            return
        if isinstance(obj, DiagnosticInstance):
            for svc in obj.services:
                self._collect_services(svc, result)
            return
        if isinstance(obj, DiagnosticGroup):
            for inst in obj.diagInst:
                self._collect_services(inst, result)
            return
        if isinstance(obj, EcuModel):
            for diag in obj.diag_list:
                self._collect_services(diag, result)
            return
        # 回退：遍历可迭代属性
        if hasattr(obj, '__dict__'):
            for v in obj.__dict__.values():
                if isinstance(v, (list, tuple)):
                    for item in v:
                        self._collect_services(item, result)

    # ─────────────────────────── 公共 API ───────────────────────────

    @property
    def model(self) -> CddModel:
        """完整的 CDD 数据模型"""
        return self._model

    @property
    def ecu(self) -> Optional[EcuModel]:
        """ECU 诊断模型"""
        return self._model.ecu if self._model else None

    @property
    def services(self) -> NamedItemList[DiagnosticService]:
        """所有诊断服务（支持按 qualifier 属性访问）

        Example:
            >>> db.services[0]                      # 按索引
            >>> db.services.ReadDTCInformation       # 按名称
            >>> db.services.by_name("ReadDTCInfo")   # 按原名搜索
        """
        return self._services

    @property
    def warnings(self) -> list[str]:
        """非严格模式下收集的警告"""
        return list(self._warnings)

    @property
    def is_frozen(self) -> bool:
        """数据库是否已冻结"""
        return self._frozen

    def find_service(self, qualifier: str) -> Optional[DiagnosticService]:
        """按 qualifier 精确查找服务"""
        return self._services.by_name(qualifier)

    def search_services(self, keyword: str) -> list[DiagnosticService]:
        """按关键词模糊搜索服务"""
        return self._services.search(keyword)

    # ─────────────────────────── 序列化支持 ───────────────────────────

    def __getstate__(self):
        """支持 pickle 序列化"""
        state = self.__dict__.copy()
        state.pop('_transformer_registry', None)
        return state

    def __setstate__(self, state):
        """从 pickle 反序列化恢复"""
        self.__dict__.update(state)
        self._transformer_registry = TransformerRegistry()

    def __repr__(self):
        svc_count = len(self._services) if self._services else 0
        ecu_name = ""
        if self._model and self._model.ecu:
            try:
                ecu_name = self._model.ecu.name.tuv[0].value
            except (AttributeError, IndexError):
                ecu_name = str(self._model.ecu.id)
        return f"<CddDatabase ecu={ecu_name!r} services={svc_count} frozen={self._frozen}>"
