"""诊断消息和服务模型

DiagnosticMessage: 诊断报文（请求/正响应/负响应）
DiagnosticService: 诊断服务（用户主要交互的对象）
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Any

from .base import IdentifiableElement, CodedElement, Quantity, ByteOrder
from .containers import StructElement, MultiplexedElement, NumIterElement, DidElement
from .candela import Name, Desc
from ..codec import EncodeState, DecodeState


@dataclass(frozen=True)
class DiagnosticMessage:
    """诊断报文 — 请求/正响应/负响应"""
    name: Name
    id: Optional[str] = None
    description: Optional[Desc] = None
    qualifier: Optional[str] = None
    elements: tuple = ()

    @staticmethod
    def _default_value(elem: Any) -> int:
        """元素默认值：constvalue > textmap首项 > comp.s > 0"""
        constvalue = getattr(elem, 'constvalue', None)
        if constvalue is not None:
            return int(constvalue)

        textmap = getattr(elem, 'textmap', None)
        if textmap:
            for tm in textmap:
                s_val = getattr(tm, 's', None)
                if s_val is not None:
                    try:
                        return int(s_val)
                    except (TypeError, ValueError):
                        return 0

        comp = getattr(elem, 'comp', None)
        if comp is not None and getattr(comp, 's', None) is not None:
            try:
                return int(comp.s)
            except (TypeError, ValueError):
                return 0

        return 0

    @classmethod
    def _encode_element_to_state(cls, state: EncodeState, elem: Any) -> None:
        """递归将元素写入编码状态机（bit级游标）。"""
        if isinstance(elem, (StructElement, DidElement)):
            for child in getattr(elem, 'children', ()):
                cls._encode_element_to_state(state, child)
            return

        if isinstance(elem, MultiplexedElement):
            bit_length = getattr(elem, 'bit_length', 0) or 0
            if bit_length > 0:
                selector = elem.cases[0].s if getattr(elem, 'cases', None) else 0
                state.write_bits(int(selector), bit_length, "21")
                if elem.cases and elem.cases[0].structure:
                    cls._encode_element_to_state(state, elem.cases[0].structure)
            return

        if isinstance(elem, NumIterElement):
            return

        if not isinstance(elem, CodedElement):
            return

        bit_length = getattr(elem, 'bit_length', 0) or 0
        if bit_length <= 0:
            return

        qty = getattr(elem, 'quantity', None)
        minsz = getattr(elem, 'minsz', 1) or 1
        total_bits = bit_length * minsz if (qty == Quantity.FIELD or str(qty) == 'field') else bit_length

        value = cls._default_value(elem)
        if total_bits > 0:
            max_val = (1 << min(total_bits, 64)) - 1
            value = max(0, min(value, max_val))

        is_be = not (getattr(elem, 'byte_order', ByteOrder.BIG_ENDIAN) == ByteOrder.LITTLE_ENDIAN)
        order = "21" if is_be else "12"
        state.write_bits(value, total_bits, order)

    def encode_default(self) -> bytes:
        """按模型默认值编码整条消息（使用 cdd_v2.codec.EncodeState）。"""
        state = EncodeState()
        for elem in self.elements:
            self._encode_element_to_state(state, elem)
        return state.get_bytes()

    @staticmethod
    def _element_key(elem: Any) -> str:
        """获取元素键名（优先 qualifier）。"""
        qualifier = getattr(elem, 'qualifier', None)
        if qualifier:
            return str(qualifier)
        name = getattr(elem, 'name', None)
        if name and getattr(name, 'tuv', None):
            if name.tuv and getattr(name.tuv[0], 'value', None):
                return str(name.tuv[0].value)
        elem_id = getattr(elem, 'id', None)
        if elem_id:
            return str(elem_id)
        return type(elem).__name__

    @classmethod
    def _decode_element_from_state(cls, state: DecodeState, elem: Any) -> Any:
        """递归从解码状态机读取单个元素值。"""
        if isinstance(elem, (StructElement, DidElement)):
            result = {}
            for child in getattr(elem, 'children', ()):
                key = cls._element_key(child)
                value = cls._decode_element_from_state(state, child)
                if key in result:
                    idx = 2
                    while f"{key}_{idx}" in result:
                        idx += 1
                    result[f"{key}_{idx}"] = value
                else:
                    result[key] = value
            return result

        if isinstance(elem, MultiplexedElement):
            selector_bits = getattr(elem, 'bit_length', 0) or 0
            selector = state.read_bits(selector_bits, "21") if selector_bits > 0 else 0
            matched_case = None
            for case in getattr(elem, 'cases', ()):
                case_s = getattr(case, 's', None)
                case_e = getattr(case, 'e', None)
                if case_s is None:
                    continue
                end_val = case_e if case_e is not None else case_s
                if case_s <= selector <= end_val:
                    matched_case = case
                    break

            case_payload = None
            if matched_case and getattr(matched_case, 'structure', None):
                case_payload = cls._decode_element_from_state(state, matched_case.structure)

            return {
                'selector': selector,
                'case': case_payload,
            }

        if isinstance(elem, NumIterElement):
            return []

        if not isinstance(elem, CodedElement):
            return None

        bit_length = getattr(elem, 'bit_length', 0) or 0
        if bit_length <= 0:
            return None

        qty = getattr(elem, 'quantity', None)
        minsz = getattr(elem, 'minsz', 1) or 1
        total_bits = bit_length * minsz if (qty == Quantity.FIELD or str(qty) == 'field') else bit_length

        is_be = not (getattr(elem, 'byte_order', ByteOrder.BIG_ENDIAN) == ByteOrder.LITTLE_ENDIAN)
        order = "21" if is_be else "12"
        value = state.read_bits(total_bits, order)

        return value

    def decode_values(self, data: bytes) -> dict[str, Any]:
        """按消息元素定义解码字节流，返回键值结构。"""
        state = DecodeState(source=data)
        result: dict[str, Any] = {}
        for elem in self.elements:
            key = self._element_key(elem)
            value = self._decode_element_from_state(state, elem)
            if key in result:
                idx = 2
                while f"{key}_{idx}" in result:
                    idx += 1
                result[f"{key}_{idx}"] = value
            else:
                result[key] = value
        return result


@dataclass(frozen=True)
class DiagnosticService:
    """诊断服务 — 用户主要交互的对象
    
    包含服务名称、协议模板名称、请求/响应报文等。
    """
    service_name: Name
    protocol_svc_name: Name
    id: Optional[str] = None
    description: Optional[Desc] = None
    qualifier: Optional[str] = None

    is_used: bool = False
    func: bool = False
    phys: bool = False
    resp_on_phys: bool = False
    resp_on_func: bool = False
    respsupbit: bool = False

    request: Optional[DiagnosticMessage] = None
    positive_responses: Optional[DiagnosticMessage] = None
    negative_responses: Optional[DiagnosticMessage] = None
    mayBeExec: tuple = ()
    trans: tuple = ()

    @property
    def free_parameters(self) -> list[str]:
        """获取可自由设置的参数名列表（constvalue 为 None 的元素）"""
        if self.request is None:
            return []
        return [
            elem.qualifier or elem.name.tuv[0].value
            for elem in self.request.elements
            if isinstance(elem, CodedElement) and elem.constvalue is None
        ]
