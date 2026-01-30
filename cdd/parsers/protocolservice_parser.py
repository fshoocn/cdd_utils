
from typing import Any, Callable,Dict, List,Optional, Union

from ..utils.logging import logging

from ..models.cdd_model import DiagnosticElement, DiagnosticMessage, DiagnosticService
from .base_parser import BaseParser
from ..models.candela import Name, Protocolservice, Tuv, Req

@logging
class ProtocolserviceParser(BaseParser):
    priority = 90  # 优先级较低

    def match(self, raw_obj: Any) -> bool:
        # raw_obj对象是否为 Protocolservice
        return isinstance(raw_obj, Protocolservice)


    def parse(self, raw_obj: Protocolservice, raw_data_map: Dict[str, Any], strict: bool = True, get_data_from_id: Optional[Callable[[str], Any]] = None) -> DiagnosticService:
        protocol_svc_name = raw_obj.name if raw_obj.name is not None else Name(tuv=[Tuv(lang="en-US", value="Unnamed Protocol Service Template"),Tuv(lang="zh-CN", value="未命名协议服务")])
        if raw_obj.req is None:
            request = None
        else:
            request :DiagnosticMessage = self.parse_message(raw_obj.req, raw_data_map, strict=strict, get_data_from_id=get_data_from_id)

        if raw_obj.pos is None:
            positive_responses = None
        else:
            positive_responses :DiagnosticMessage = self.parse_message(raw_obj.pos, raw_data_map, strict=strict, get_data_from_id=get_data_from_id)

        if raw_obj.neg is None:
            negative_responses = None
        else:
            negative_responses :DiagnosticMessage = self.parse_message(raw_obj.neg, raw_data_map, strict=strict, get_data_from_id=get_data_from_id)

        return DiagnosticService(
            id=raw_obj.id,
            service_name=Name(tuv=[Tuv(lang="en-US", value="Unnamed Service"),Tuv(lang="zh-CN", value="未命名服务")]),
            protocol_svc_name=protocol_svc_name,
            qualifier=raw_obj.qual,
            description=raw_obj.desc,
            is_used=False,

            request=request,
            positive_responses=positive_responses,
            negative_responses=negative_responses,
        )
    
    def parse_message(self, raw_obj: Req, raw_data_map: Dict[str, Any], strict: bool = True, get_data_from_id: Optional[Callable[[str], Any]] = None) -> DiagnosticMessage:
        elements: List[DiagnosticElement] = []
        for item in raw_obj.items:
            element: DiagnosticElement = get_data_from_id(item.id)
            elements.append(element)
            self._logger.debug(f"element: {element}")

        return DiagnosticMessage(
            name=raw_obj.name if raw_obj.name is not None else Name(tuv=[Tuv(lang="en-US", value="Unnamed Message"),Tuv(lang="zh-CN", value="未命名报文")]),
            id=raw_obj.id if hasattr(raw_obj, 'id') else None,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            elements=elements
        )