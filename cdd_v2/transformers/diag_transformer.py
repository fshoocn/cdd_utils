"""Diagclass / Diaginst → DiagnosticGroup / DiagnosticInstance 转换器"""
from __future__ import annotations

import copy
import dataclasses
from typing import Any, List, Optional, Union

from .base import BaseTransformer
from ..compat import (
    Diagclass, Diaginst, Dcltmpl, Dclsrvtmpl, Shstatic, Shproxy,
    Name, Tuv, Service, Staticvalue,
)
from ..models.ecu import DiagnosticGroup, DiagnosticInstance
from ..models.messages import DiagnosticService, DiagnosticMessage
from ..models.base import IdentifiableElement, CodedElement
from ..models.containers import StructElement
from ..registry import ObjectRegistry
from ..utils.helpers import default_name


class DiagTransformer(BaseTransformer):
    """将 Diagclass/Diaginst 转换为 DiagnosticGroup/DiagnosticInstance"""

    priority = 91
    handles_type = Diagclass

    def match(self, raw_obj: Any) -> bool:
        return isinstance(raw_obj, (Diagclass, Diaginst))

    def transform(self, raw_obj: Union[Diagclass, Diaginst], registry: ObjectRegistry,
                  warnings: list, strict: bool = True) -> Any:
        if isinstance(raw_obj, Diagclass):
            return self._transform_diagclass(raw_obj, registry, warnings, strict)
        elif isinstance(raw_obj, Diaginst):
            return self._transform_diaginst(raw_obj, registry, warnings, strict)
        else:
            raise TypeError(f"不支持的类型: {type(raw_obj)}")

    def _transform_diagclass(self, raw_obj: Diagclass, registry: ObjectRegistry,
                              warnings: list, strict: bool) -> DiagnosticGroup:
        name = raw_obj.name or default_name("Unnamed DiagClass", "未命名诊断类")

        instances = self._resolve_children(
            raw_obj.diaginst, registry, warnings, strict,
            context="DiagClass ",
        )

        return DiagnosticGroup(
            id=raw_obj.id,
            name=name,
            qualifier=raw_obj.qual,
            description=raw_obj.desc,
            diagInst=tuple(instances),
        )

    def _transform_diaginst(self, raw_obj: Diaginst, registry: ObjectRegistry,
                              warnings: list, strict: bool) -> DiagnosticInstance:
        name = raw_obj.name or default_name("Unnamed DiagInst", "未命名诊断实例")

        # 获取模板
        dcltmpl: Dcltmpl = registry.get_raw(raw_obj.tmplref)
        if dcltmpl is None:
            msg = f"DiagInst {raw_obj.id}: 模板未找到 tmplref={raw_obj.tmplref}"
            if strict:
                raise ValueError(msg)
            warnings.append(msg)
            return DiagnosticInstance(
                id=raw_obj.id, name=name, description=raw_obj.desc,
                qualifier=raw_obj.qual, services=(),
            )

        # 解析协议服务（递归确保 Protocolservice 已转换）
        protocol_services: list[DiagnosticService] = []
        for dclsrvtmpl in dcltmpl.dclsrvtmpl:
            svc_model = self._resolve_one(
                dclsrvtmpl.tmplref, registry, warnings, strict,
                context="DiagInst 服务 ",
            )
            if svc_model is None:
                msg = f"DiagInst: 服务未找到 tmplref={dclsrvtmpl.tmplref}"
                if strict:
                    raise ValueError(msg)
                warnings.append(msg)
                continue

            # 需要一个可修改的副本来覆盖属性
            # 由于 frozen=True，需要通过 dataclasses.replace 创建新对象
            new_service = svc_model
            
            if raw_obj.service:
                for svc_config in raw_obj.service:
                    if svc_config.tmplref == dclsrvtmpl.id:
                        overrides = {'is_used': True}
                        # 优先使用 SHORTCUTNAME 作为服务显示名，回退到 NAME
                        if svc_config.shortcutname:
                            overrides['service_name'] = Name(tuv=svc_config.shortcutname.tuv)
                        elif svc_config.name:
                            overrides['service_name'] = svc_config.name
                        # 优先使用 SHORTCUTQUAL 作为 qualifier，回退到 QUAL
                        if svc_config.shortcutqual:
                            overrides['qualifier'] = svc_config.shortcutqual
                        elif svc_config.qual:
                            overrides['qualifier'] = svc_config.qual
                        if svc_config.desc:
                            overrides['description'] = svc_config.desc
                        if svc_config.id:
                            overrides['id'] = svc_config.id
                        if svc_config.func is not None:
                            overrides['func'] = bool(svc_config.func)
                        if svc_config.phys is not None:
                            overrides['phys'] = bool(svc_config.phys)
                        if svc_config.resp_on_phys is not None:
                            overrides['resp_on_phys'] = bool(svc_config.resp_on_phys)
                        if svc_config.resp_on_func is not None:
                            overrides['resp_on_func'] = bool(svc_config.resp_on_func)
                        if svc_config.may_be_exec:
                            try:
                                val_str = svc_config.may_be_exec.strip('()')
                                if val_str:
                                    overrides['mayBeExec'] = tuple(
                                        int(x.strip()) for x in val_str.split(',') if x.strip()
                                    )
                            except ValueError:
                                pass
                        if svc_config.trans:
                            try:
                                val_str = svc_config.trans.strip('()')
                                if val_str:
                                    overrides['trans'] = tuple(
                                        int(x.strip()) for x in val_str.split(',') if x.strip()
                                    )
                            except ValueError:
                                pass
                        new_service = dataclasses.replace(svc_model, **overrides)
                        break

            protocol_services.append(new_service)

        # 处理 shstatic 映射
        if dcltmpl.shstatic and raw_obj.staticvalue:
            static_val = raw_obj.staticvalue
            if static_val.shstaticref == dcltmpl.shstatic.id:
                protocol_services = self._apply_shstatic_mapping(
                    value=static_val.v,
                    shstatic=dcltmpl.shstatic,
                    services=protocol_services,
                )

        # 处理 shproxy 映射（递归确保元素已转换）
        for item in raw_obj.items:
            item_id = getattr(item, 'id', None) or getattr(item, 'oid', None)
            if item_id:
                element = self._resolve_one(
                    item_id, registry, warnings, strict,
                    context="DiagInst shproxy ",
                )
                if element is not None:
                    shproxyref = getattr(item, 'shproxyref', None)
                    for shproxy in dcltmpl.shproxy:
                        if shproxy.id == shproxyref:
                            protocol_services = self._apply_shproxy_mapping(
                                inst_element=element,
                                shproxy=shproxy,
                                services=protocol_services,
                            )

        return DiagnosticInstance(
            id=raw_obj.id,
            name=name,
            description=raw_obj.desc,
            qualifier=raw_obj.qual,
            services=tuple(protocol_services),
        )

    def _apply_shstatic_mapping(
        self,
        value: int,
        shstatic: Shstatic,
        services: list[DiagnosticService],
    ) -> list[DiagnosticService]:
        """应用静态映射（支持嵌套替换）"""
        if not shstatic.staticcompref:
            return services

        target_idrefs = {ref.idref for ref in shstatic.staticcompref}

        # 第一遍：从所有服务元素中找到匹配的元素来创建模板
        template_element = None
        for service in services:
            if template_element:
                break
            for msg_attr in ('request', 'positive_responses', 'negative_responses'):
                msg = getattr(service, msg_attr)
                if msg:
                    template_element = self._find_template_element(
                        msg.elements, target_idrefs, value, shstatic.id
                    )
                    if template_element:
                        break

        if template_element is None:
            return services

        # 第二遍：递归替换
        new_services = []
        for service in services:
            new_service = service
            for msg_attr in ('request', 'positive_responses', 'negative_responses'):
                msg = getattr(service, msg_attr)
                if msg is None:
                    continue
                new_elements, changed = self._replace_in_elements(
                    msg.elements, target_idrefs, template_element
                )
                if changed:
                    new_msg = dataclasses.replace(msg, elements=tuple(new_elements))
                    new_service = dataclasses.replace(new_service, **{msg_attr: new_msg})
            new_services.append(new_service)
        return new_services

    @staticmethod
    def _find_template_element(elements, target_idrefs, value, shstatic_id):
        """在元素树中查找第一个匹配 target_idrefs 的元素并创建模板"""
        for elem in elements:
            elem_id = getattr(elem, 'id', None)
            if elem_id in target_idrefs:
                return dataclasses.replace(elem, id=shstatic_id, constvalue=value)
            if hasattr(elem, 'children') and elem.children:
                result = DiagTransformer._find_template_element(
                    elem.children, target_idrefs, value, shstatic_id
                )
                if result:
                    return result
        return None

    def _apply_shproxy_mapping(
        self,
        inst_element: Any,
        shproxy: Shproxy,
        services: list[DiagnosticService],
    ) -> list[DiagnosticService]:
        """应用代理映射"""
        target_idrefs = {ref.idref for ref in shproxy.proxycompref}

        # 创建替换元素
        overrides = {'id': shproxy.id}
        if shproxy.name:
            overrides['name'] = shproxy.name
        if shproxy.qual:
            overrides['qualifier'] = shproxy.qual
        if shproxy.desc:
            overrides['description'] = shproxy.desc
        if shproxy.dest:
            overrides['spec'] = shproxy.dest

        try:
            replacement = dataclasses.replace(inst_element, **overrides)
        except (TypeError, Exception):
            replacement = inst_element

        new_services = []
        for service in services:
            new_service = service
            for msg_attr in ('request', 'positive_responses', 'negative_responses'):
                msg = getattr(service, msg_attr)
                if msg is None:
                    continue
                new_elements, changed = self._replace_in_elements(
                    msg.elements, target_idrefs, replacement
                )
                if changed:
                    new_msg = dataclasses.replace(msg, elements=tuple(new_elements))
                    new_service = dataclasses.replace(new_service, **{msg_attr: new_msg})
            new_services.append(new_service)
        return new_services

    def _replace_in_elements(
        self,
        elements: tuple,
        target_idrefs: set,
        replacement: Any,
    ) -> tuple:
        """递归替换 elements 中 id 匹配 target_idrefs 的元素（含嵌套子元素）"""
        new_elements = list(elements)
        changed = False
        for i, elem in enumerate(new_elements):
            elem_id = getattr(elem, 'id', None)
            if elem_id in target_idrefs:
                new_elements[i] = replacement
                changed = True
            elif hasattr(elem, 'children') and elem.children:
                new_children, child_changed = self._replace_in_elements(
                    elem.children, target_idrefs, replacement
                )
                if child_changed:
                    new_elements[i] = dataclasses.replace(elem, children=tuple(new_children))
                    changed = True
        return new_elements, changed
