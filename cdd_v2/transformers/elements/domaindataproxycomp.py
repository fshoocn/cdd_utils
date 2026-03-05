"""Domaindataproxycomp → 模型元素转换器

DOMAINDATAPROXYCOMP 是域数据代理组件，根据 dest 属性值关联到 ECU 的
FAULTMEMORY 数据：
  - dest='edrn' → TextTableElement（ExtendedDataRecord 记录号映射）
  - dest='ed'   → StructElement（ExtendedDataRecord 数据结构）
  - dest='srn'  → TextTableElement（SnapshotRecord 记录号映射）
  - dest='sd'   → StructElement（SnapshotRecord 数据结构）
  - 其他 dest   → 回退为 CodedElement（默认编码元素）
"""
from typing import Any, Optional

from ..base import BaseTransformer
from ...compat import Domaindataproxycomp, Name, Tuv, Text, Textmap, Ecu
from ...models.base import CodedElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ...models.elements import TextTableElement
from ...models.containers import StructElement, DidElement
from ...registry import ObjectRegistry
from ...utils.helpers import default_name


# 常见域代理类型的默认位长度
_DOMAIN_DEFAULTS = {
    'edrn': 8,        # Extended Data Record Number (1 byte)
    'ed': 8,          # Extended Data (可变，默认 1 byte)
    'srn': 8,         # Snapshot Record Number (1 byte)
    'sd': 8,          # Snapshot Data (可变，默认 1 byte)
    'dtc': 24,        # DTC code (3 bytes)
    'dtcStatus': 8,   # DTC status mask (1 byte)
    'sid': 8,         # Service ID (1 byte)
    'sub': 8,         # Sub-function (1 byte)
    'did': 16,        # Data Identifier (2 bytes)
    'rid': 16,        # Routine Identifier (2 bytes)
    'data': 8,        # 通用数据 (可变，默认 1 byte)
    'any': 8,         # 任意数据 (可变，默认 1 byte)
}


class DomaindataproxycompTransformer(BaseTransformer):
    """将 Domaindataproxycomp（域数据代理组件）转换为对应的模型元素

    当 ECU 存在 FAULTMEMORY 时，edrn/ed/srn/sd 类型会自动关联到
    EXTENDEDDATARECORDS / SNAPSHOTRECORDS 的实际数据。
    """

    priority = 50
    handles_type = Domaindataproxycomp

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Domaindataproxycomp)

    def transform(self, raw_obj: Domaindataproxycomp, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> Any:
        name = raw_obj.name or default_name("Unnamed DomainData Proxy", "未命名域数据代理组件")

        dest = raw_obj.dest or ''
        faultmemory = self._find_faultmemory(registry)

        # 根据 dest 类型分发
        if dest == 'edrn' and faultmemory:
            result = self._resolve_edrn(raw_obj, name, faultmemory, registry, warnings, strict)
            if result is not None:
                return result

        elif dest == 'ed' and faultmemory:
            result = self._resolve_ed(raw_obj, name, faultmemory, registry, warnings, strict)
            if result is not None:
                return result

        elif dest == 'srn' and faultmemory:
            result = self._resolve_srn(raw_obj, name, faultmemory, registry, warnings, strict)
            if result is not None:
                return result

        elif dest == 'sd' and faultmemory:
            result = self._resolve_sd(raw_obj, name, faultmemory, registry, warnings, strict)
            if result is not None:
                return result

        # 回退到默认 CodedElement
        return self._default_coded_element(raw_obj, name, dest)

    # ─── FAULTMEMORY 查找 ───

    def _find_faultmemory(self, registry: ObjectRegistry):
        """从注册表中查找 ECU 的 FAULTMEMORY（使用 registry 自身缓存避免泄漏）"""
        # 利用 registry 对象上的属性做缓存，生命周期与 registry 一致
        cache = getattr(registry, '_faultmemory_cache', None)
        if cache is not None:
            return cache

        result = None
        for obj_id in registry.raw_ids:
            raw = registry.get_raw(obj_id)
            if isinstance(raw, Ecu) and raw.faultmemory:
                result = raw.faultmemory
                break

        # 缓存结果到 registry 上（包括 None，避免重复扫描）
        registry._faultmemory_cache = result
        return result

    # ─── dest='edrn': ExtendedDataRecord 记录号 → TextTableElement ───

    def _resolve_edrn(self, raw_obj, name, faultmemory, registry, warnings, strict):
        """将 ExtendedDataRecord 的 rn/name 映射为 TextTableElement"""
        edrs = faultmemory.extendeddatarecords
        if not edrs or not edrs.extendeddatarecord:
            return None

        textmap_entries = []
        for edr in edrs.extendeddatarecord:
            rn = edr.rn
            edr_name = edr.name
            text = Text(tuv=edr_name.tuv) if edr_name else Text(
                tuv=[Tuv(lang="en-US", value=f"Record {rn}")]
            )
            textmap_entries.append(Textmap(s=rn, e=rn, text=text))

        return TextTableElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec=raw_obj.dest,
            must=raw_obj.must,
            bit_length=8,
            minsz=1,
            maxsz=1,
            quantity=Quantity.ATOM,
            display_format=DisplayFormat.HEX,
            encoding=Encoding.UNSIGNED,
            byte_order=ByteOrder.BIG_ENDIAN,
            textmap=tuple(textmap_entries),
        )

    # ─── dest='ed': ExtendedData → StructElement ───

    def _resolve_ed(self, raw_obj, name, faultmemory, registry, warnings, strict):
        """解析第一个 EDR 的 STRUCTURE 子元素为 StructElement"""
        edrs = faultmemory.extendeddatarecords
        if not edrs or not edrs.extendeddatarecord:
            return None

        # 使用第一个 EDR 的结构作为代表
        edr = edrs.extendeddatarecord[0]
        if not edr.structure or not edr.structure.items:
            return None

        children = self._resolve_children(
            edr.structure.items, registry, warnings, strict,
            context=f"FAULTMEMORY EDR[rn={edr.rn}] ",
        )
        if not children:
            return None

        return StructElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec=raw_obj.dest,
            must=raw_obj.must,
            children=tuple(children),
        )

    # ─── dest='srn': SnapshotRecord 记录号 → TextTableElement ───

    def _resolve_srn(self, raw_obj, name, faultmemory, registry, warnings, strict):
        """将 SnapshotRecord 的 rn/name 映射为 TextTableElement"""
        srs = faultmemory.snapshotrecords
        if not srs or not srs.specificsnapshotrecord:
            return None

        textmap_entries = []
        for sr in srs.specificsnapshotrecord:
            rn = sr.rn
            sr_name = sr.name
            text = Text(tuv=sr_name.tuv) if sr_name else Text(
                tuv=[Tuv(lang="en-US", value=f"Snapshot {rn}")]
            )
            textmap_entries.append(Textmap(s=rn, e=rn, text=text))

        return TextTableElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec=raw_obj.dest,
            must=raw_obj.must,
            bit_length=8,
            minsz=1,
            maxsz=1,
            quantity=Quantity.ATOM,
            display_format=DisplayFormat.HEX,
            encoding=Encoding.UNSIGNED,
            byte_order=ByteOrder.BIG_ENDIAN,
            textmap=tuple(textmap_entries),
        )

    # ─── dest='sd': SnapshotData → StructElement ───

    def _resolve_sd(self, raw_obj, name, faultmemory, registry, warnings, strict):
        """解析第一个 SnapshotRecord 的公共快照数据

        支持两种 COMMONSNAPSHOTDATA 格式：
        1. AnyCommonSnapshotData — 带 STRUCTURE / items 内联结构
        2. DidCommonSnapshotData — 带 SNAPSHOTDATADIDREF DID 引用列表
        """
        srs = faultmemory.snapshotrecords
        if not srs or not srs.specificsnapshotrecord:
            return None

        # 取第一个快照记录的 csdRef → 查找 COMMONSNAPSHOTDATAPOOL
        sr = srs.specificsnapshotrecord[0]
        csd_ref = sr.csd_ref
        if not csd_ref:
            return None

        csd = self._find_common_snapshot_data(faultmemory, csd_ref)
        if not csd:
            return None

        # 方式一: AnyCommonSnapshotData — 内联 STRUCTURE
        if getattr(csd, 'structure', None) and csd.structure.items:
            children = self._resolve_children(
                csd.structure.items, registry, warnings, strict,
                context=f"FAULTMEMORY SNAPSHOT[csdRef={csd_ref}] ",
            )
        # 方式二: DidCommonSnapshotData — DID 引用列表
        elif getattr(csd, 'snapshotdatadidref', None):
            children = self._resolve_did_snapshot(
                csd, registry, warnings, strict,
            )
        else:
            return None

        if not children:
            return None

        return StructElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec=raw_obj.dest,
            must=raw_obj.must,
            children=tuple(children),
        )

    def _resolve_did_snapshot(self, csd, registry, warnings, strict):
        """将 DidCommonSnapshotData 的 SNAPSHOTDATADIDREF 解析为 DidElement 列表"""
        children = []
        for did_ref_entry in csd.snapshotdatadidref:
            did_ref = did_ref_entry.did_ref
            if not did_ref:
                continue

            did = registry.get_raw(did_ref)
            if did is None:
                warnings.append(f"找不到快照 DID 引用: {did_ref}")
                continue

            # 解析 DID 的 STRUCTURE 子元素
            did_children = []
            if did.structure and did.structure.items:
                did_children = self._resolve_children(
                    did.structure.items, registry, warnings, strict,
                    context=f"SNAPSHOT DID[{did_ref}] ",
                )

            did_name = did.name or Name(
                tuv=[Tuv(lang="en-US", value=f"DID {did.n or 0:04X}")]
            )
            did_number = did.n if did.n is not None else 0

            children.append(DidElement(
                id=did_ref,
                name=did_name,
                description=did.desc,
                qualifier=did.qual,
                did=did_number,
                children=tuple(did_children),
            ))

        return children

    @staticmethod
    def _find_common_snapshot_data(faultmemory, csd_ref):
        """在 COMMONSNAPSHOTDATAPOOL 中查找 id == csd_ref 的数据"""
        pool = faultmemory.commonsnapshotdatapool
        if not pool:
            return None
        for csd in pool.anycommonsnapshotdata:
            if csd.id == csd_ref:
                return csd
        for csd in pool.didcommonsnapshotdata:
            if getattr(csd, 'id', None) == csd_ref:
                return csd
        return None

    # ─── 回退默认 ───

    @staticmethod
    def _default_coded_element(raw_obj, name, dest):
        """回退到默认 CodedElement"""
        bit_length = _DOMAIN_DEFAULTS.get(dest, 8)

        return CodedElement(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            spec=raw_obj.dest,
            must=raw_obj.must,
            bit_length=bit_length,
            minsz=1,
            maxsz=1,
            quantity=Quantity.ATOM,
            display_format=DisplayFormat.HEX,
            encoding=Encoding.UNSIGNED,
            byte_order=ByteOrder.BIG_ENDIAN,
        )
