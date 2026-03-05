"""Protocolservice → DiagnosticService 转换器"""
from __future__ import annotations

import dataclasses
from typing import Any, List

from .base import BaseTransformer
from ..compat import Protocolservice, Req, Name, Tuv, Textmap, Text, Negrescode
from ..models.messages import DiagnosticMessage, DiagnosticService
from ..models.base import CodedElement, ByteOrder, DisplayFormat, Encoding, Quantity
from ..models.elements import TextTableElement
from ..registry import ObjectRegistry


class ProtocolserviceTransformer(BaseTransformer):
    """将 Protocolservice 转换为 DiagnosticService"""

    priority = 90
    handles_type = Protocolservice

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, Protocolservice)

    def transform(self, raw_obj: Protocolservice, registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> DiagnosticService:
        protocol_svc_name = raw_obj.name or Name(
            tuv=[Tuv(lang="en-US", value="Unnamed Protocol Service Template"),
                 Tuv(lang="zh-CN", value="未命名协议服务")]
        )

        request = self._transform_message(raw_obj.req, registry, warnings, strict) if raw_obj.req else None
        positive_responses = self._transform_message(raw_obj.pos, registry, warnings, strict) if raw_obj.pos else None
        negative_responses = self._transform_message(raw_obj.neg, registry, warnings, strict) if raw_obj.neg else None

        # 将 NEGRESCODEPROXIES 注入到 NEG 消息的 resCode 元素中
        if negative_responses and raw_obj.negrescodeproxies:
            negative_responses = self._inject_nrc_textmap(
                negative_responses, raw_obj, registry, warnings,
            )

        return DiagnosticService(
            id=raw_obj.id,
            service_name=Name(
                tuv=[Tuv(lang="en-US", value="Unnamed Service"),
                     Tuv(lang="zh-CN", value="未命名服务")]
            ),
            protocol_svc_name=protocol_svc_name,
            qualifier=raw_obj.qual,
            description=raw_obj.desc,
            is_used=False,
            request=request,
            positive_responses=positive_responses,
            negative_responses=negative_responses,
        )

    def _transform_message(self, raw_msg: Req, registry: ObjectRegistry,
                           warnings: list, strict: bool) -> DiagnosticMessage:
        """转换消息（请求/响应）— 递归解析所有子元素"""
        elements = self._resolve_children(
            raw_msg.items, registry, warnings, strict,
            context="Message ",
        )

        return DiagnosticMessage(
            name=raw_msg.name or Name(
                tuv=[Tuv(lang="en-US", value="Unnamed Message"),
                     Tuv(lang="zh-CN", value="未命名报文")]
            ),
            id=getattr(raw_msg, 'id', None),
            description=raw_msg.desc,
            qualifier=raw_msg.qual,
            elements=tuple(elements),
        )

    def _inject_nrc_textmap(
        self,
        neg_msg: DiagnosticMessage,
        raw_obj: Protocolservice,
        registry: ObjectRegistry,
        warnings: list,
    ) -> DiagnosticMessage:
        """将 Protocolservice 级别的 NEGRESCODEPROXIES 注入到 NEG 消息中的 resCode 元素。

        CDD 结构中，NEG 消息内的 SIMPLEPROXYCOMP(dest='resCode') 只是一个占位
        代理，真正的 NRC 条目存储在 Protocolservice.negrescodeproxies 中。
        本方法将 CodedElement(spec='resCode') 替换为 TextTableElement，
        并携带从 NEGRESCODEPROXY → NEGRESCODE 解析出的 textmap。
        """
        nrc_proxies = raw_obj.negrescodeproxies
        if not nrc_proxies or not nrc_proxies.negrescodeproxy:
            return neg_msg

        # 构建 textmap
        textmap_list: list[Textmap] = []
        for proxy in nrc_proxies.negrescodeproxy:
            if not proxy.idref:
                continue
            negrescode: Negrescode | None = registry.get_raw(proxy.idref)
            if negrescode is None:
                warnings.append(f"ProtocolService NRC: 找不到 NEGRESCODE 引用 {proxy.idref}")
                continue
            textmap_list.append(Textmap(
                s=negrescode.v,
                e=negrescode.v,
                text=Text(tuv=negrescode.name.tuv) if negrescode.name else None,
                addinfo=None,
            ))

        if not textmap_list:
            return neg_msg

        # 替换 NEG 消息中 spec='resCode' 的 CodedElement → TextTableElement
        new_elements = list(neg_msg.elements)
        changed = False
        for i, elem in enumerate(new_elements):
            spec = getattr(elem, 'spec', None)
            if spec == 'resCode' and isinstance(elem, CodedElement):
                replacement = TextTableElement(
                    id=elem.id,
                    name=elem.name,
                    description=elem.description,
                    qualifier=elem.qualifier,
                    spec=elem.spec,
                    must=elem.must,
                    bit_length=elem.bit_length,
                    minsz=elem.minsz,
                    maxsz=elem.maxsz,
                    display_format=elem.display_format,
                    encoding=elem.encoding,
                    byte_order=elem.byte_order,
                    quantity=elem.quantity,
                    textmap=tuple(textmap_list),
                )
                new_elements[i] = replacement
                changed = True

        if changed:
            return dataclasses.replace(neg_msg, elements=tuple(new_elements))
        return neg_msg
