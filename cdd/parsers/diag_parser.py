
import copy
import json
from dataclasses import asdict
from typing import Any, Callable, Dict, List, Optional, Union

from ..utils.logging import logging

from ..models.cdd_model import DiagnosticElement, DiagnosticGroup, DiagnosticInstance, DiagnosticMessage, DiagnosticService

from ..models.candela import Dclsrvtmpl, Dcltmpl, Diagclass, Diaginst, Muxcompcont, Name, Protocolservice, Service, Shproxy, Shstatic, Simplecompcont, Staticvalue, Tuv
from .base_parser import BaseParser

@logging
class DiagParser(BaseParser):
    """
    解析 Diagclass（诊断类）和 Diaginst（诊断实例）为 DiagnosticGroup 和 DiagnosticInstance。
    
    核心职责：
    1. 解析 Diagclass 为 DiagnosticGroup，包含多个 DiagnosticInstance
    2. 解析 Diaginst 为 DiagnosticInstance，包含多个 DiagnosticService
    3. 根据 Dcltmpl（模板）的 shstatic 和 shproxy 配置，将静态值和代理数据替换到服务模板中
    
    数据流程:
    - Diaginst.tmplref -> Dcltmpl（诊断类模板）
    - Dcltmpl.dclsrvtmpl[].tmplref -> Protocolservice（协议服务模板）
    - Dcltmpl.shstatic -> 静态值映射配置（通常用于子功能码）
    - Dcltmpl.shproxy[] -> 代理数据映射配置（将实例数据替换到模板中）
    - Diaginst.staticvalue -> 具体的静态值（如子功能码的值）
    - Diaginst.items -> 实例中的数据元素
    - Diaginst.service[] -> 服务属性覆盖（func、phys、响应等）
    """
    priority = 91  # 优先级较高

    def match(self, raw_obj: Any) -> bool:
        """判断对象是否为 Diagclass 或 Diaginst"""
        return isinstance(raw_obj, (Diagclass, Diaginst))


    def parse(self, raw_obj: Union[Diagclass, Diaginst], raw_data_map: Dict[str, Any], strict: bool = True, get_data_from_id: Optional[Callable[[str], Any]] = None) -> Union[DiagnosticGroup, DiagnosticInstance]:
        if isinstance(raw_obj, Diagclass):
            return self.parse_diagclass(raw_obj, raw_data_map, strict, get_data_from_id)
        elif isinstance(raw_obj, Diaginst):
            return self.parse_diaginst(raw_obj, raw_data_map, strict, get_data_from_id)
        else:
            raise TypeError(f"不支持的类型: {type(raw_obj)}")
    
    def parse_diagclass(self, raw_obj: Diagclass, raw_data_map: Dict[str, Any], strict: bool = True, get_data_from_id: Optional[Callable[[str], Any]] = None) -> DiagnosticGroup:
        """
        解析 Diagclass 为 DiagnosticGroup
        
        Diagclass 是诊断类，包含多个诊断实例（Diaginst）。
        例如：Sessions 诊断类包含 DefaultSession、ExtendedSession 等多个实例。
        """
        group: DiagnosticGroup = DiagnosticGroup(
            id=raw_obj.id,
            name=raw_obj.name if raw_obj.name is not None else Name(
                tuv=[
                    Tuv(lang="en-US", value="Unnamed DiagClass"),
                    Tuv(lang="zh-CN", value="未命名诊断类")
                ]
            ),
            qualifier=raw_obj.qual,
            description=raw_obj.desc,
            diagInst=[],
        )
        
        for diaginst in raw_obj.diaginst:
            instance: DiagnosticInstance = self.parse_diaginst(
                diaginst, raw_data_map, strict=strict, get_data_from_id=get_data_from_id
            )
            group.diagInst.append(instance)
            self._logger.debug(f"解析诊断实例: {instance.name.tuv[0].value if instance.name and instance.name.tuv else 'N/A'}")
        
        return group

    def parse_diaginst(self, raw_obj: Diaginst, raw_data_map: Dict[str, Any], strict: bool = True, get_data_from_id: Optional[Callable[[str], Any]] = None) -> DiagnosticInstance:
        name = raw_obj.name if raw_obj.name is not None else Name(
            tuv=[
                Tuv(lang="en-US", value="Unnamed DiagInst"),
                Tuv(lang="zh-CN", value="未命名诊断实例")
            ]
        )
        
        # 1. 获取诊断类模板
        dcltmpl: Dcltmpl = raw_data_map.get(raw_obj.tmplref)
        
        # 2. 根据模板获取所有协议服务并深拷贝（避免修改原始模板）
        protocol_services: List[DiagnosticService] = []
        
        for dclsrvtmpl in dcltmpl.dclsrvtmpl:
            # 用户提示: get_data_from_id 返回的已是独立副本，无需再次 deepcopy
            new_service: DiagnosticService = get_data_from_id(dclsrvtmpl.tmplref)
            
            # 使用 Diaginst.service 配置覆盖模板属性
            # 查找对应 tmplref 的服务配置
            if raw_obj.service:
                for svc_config in raw_obj.service:
                    if svc_config.tmplref == dclsrvtmpl.id:  # 注意: 这里比较的是 dclsrvtmpl 的 ID
                        self._logger.debug(f"覆盖服务属性: {new_service.service_name.tuv[0].value if new_service.service_name else 'N/A'}")
                        new_service.is_used = True
                        # 覆盖基本属性
                        if svc_config.name:
                            new_service.service_name = svc_config.name
                        if svc_config.qual:
                            new_service.qualifier = svc_config.qual
                        if svc_config.desc:
                            new_service.description = svc_config.desc
                        if svc_config.id:
                            new_service.id = svc_config.id
                            
                        # 覆盖控制属性
                        if svc_config.func is not None:
                            new_service.func = bool(svc_config.func)
                        if svc_config.phys is not None:
                            new_service.phys = bool(svc_config.phys)
                        if svc_config.resp_on_phys is not None:
                            new_service.resp_on_phys = bool(svc_config.resp_on_phys)
                        if svc_config.resp_on_func is not None:
                            new_service.resp_on_func = bool(svc_config.resp_on_func)
                            
                        # 转换状态组引用 (mayBeExec, trans)
                        # 格式示例: '(1,2,3)' -> [1, 2, 3]
                        if svc_config.may_be_exec:
                            try:
                                val_str = svc_config.may_be_exec.strip('()')
                                if val_str:
                                    new_service.mayBeExec = [int(x.strip()) for x in val_str.split(',') if x.strip()]
                            except ValueError as e:
                                self._logger.warning(f"解析 mayBeExec 失败: {svc_config.may_be_exec}, error={e}")

                        if svc_config.trans:
                            try:
                                val_str = svc_config.trans.strip('()')
                                if val_str:
                                    new_service.trans = [int(x.strip()) for x in val_str.split(',') if x.strip()]
                            except ValueError as e:
                                self._logger.warning(f"解析 trans 失败: {svc_config.trans}, error={e}")
                        
                        break
            
            protocol_services.append(new_service)

        # 4. 应用静态映射（shstatic）
        # 提取 raw_obj.staticvalue 的 v 和 shstaticref 数据，
        # 根据 shstaticref 找到对应的 Shstatic 映射信息
        if dcltmpl.shstatic and raw_obj.staticvalue:
            static_val = raw_obj.staticvalue
            # static_val.shstaticref 应该指向 dcltmpl.shstatic.id
            if static_val.shstaticref == dcltmpl.shstatic.id:
                self.apply_shstatic_mapping(
                    value=static_val.v,
                    shstatic=dcltmpl.shstatic,
                    services=protocol_services
                )
                self._logger.debug(f"应用静态映射: shstaticref={static_val.shstaticref}, v={static_val.v}")

        # 3. 解析 Diaginst 下的Simplecompcont, Muxcompcont数据元素，用于代理映射
        for item in raw_obj.items:
            item_id = getattr(item, 'id', None) or getattr(item, 'oid', None)
            element: DiagnosticElement = get_data_from_id(item_id)
            shproxyref = getattr(item, 'shproxyref', None)
            for shproxy in dcltmpl.shproxy:
                if shproxy.id == shproxyref:
                    self.apply_shproxy_mapping(
                            inst_elements=element,
                            shproxy=shproxy,
                            services=protocol_services
                        )
                    
        # 替换基础信息，例如Name等

        return DiagnosticInstance(
                id=raw_obj.id,
                name=name,
                description=raw_obj.desc,
                qualifier=raw_obj.qual,
                services=protocol_services,
            )

    # 修改静态映射
    def apply_shstatic_mapping(self, value: int, shstatic: Shstatic, services: List[DiagnosticService]):
        """
        应用静态映射，将常量值设置到服务的对应元素中。
        
        Shstatic.staticcompref 指向 services 下所有的 req、pos、neg 的 
        DiagnosticMessage 下的 elements 里面元素的 id。
        找到第一个匹配的 element，设置其 constvalue，然后用这个对象替换所有其他匹配的元素。
        
        Args:
            value: 静态值（如子功能码）
            shstatic: 静态映射配置
            services: 服务列表
        """
        if not shstatic.staticcompref:
            return
        
        # 收集所有需要替换的 idref
        target_idrefs = {ref.idref for ref in shstatic.staticcompref}
        
        # 查找第一个匹配的元素作为模板
        template_element: Optional[DiagnosticElement] = None
        
        for service in services:
            for msg in [service.request, service.positive_responses, service.negative_responses]:
                if msg is None:
                    continue
                for i, elem in enumerate(msg.elements):
                    if elem.id in target_idrefs:
                        if template_element is None:
                            # 找到第一个匹配的元素，深拷贝并设置 constvalue
                            template_element = copy.deepcopy(elem)
                            template_element.id = shstatic.id  # 使用 shstatic.id 作为新 id
                            template_element.constvalue = value
                            self._logger.debug(
                                f"静态映射模板: id={elem.id} -> new_id={shstatic.id}, constvalue={value}"
                            )
                        # 替换当前元素
                        msg.elements[i] = template_element
                        self._logger.debug(f"替换静态元素: id={elem.id}")

    # 修改代理映射
    def apply_shproxy_mapping(
        self, 
        inst_elements: DiagnosticElement,
        shproxy: Shproxy, 
        services: List[DiagnosticService]
    ):
        """
        应用代理映射，将实例数据元素替换到服务模板的对应位置。
        
        Shproxy.proxycompref 列表中的 idref 指向模板中的代理组件位置，
        Shproxy.dest 对应实例中的数据元素 id。
        
        Args:
            inst_elements: 实例中的数据元素字典 {id: DiagnosticElement}
            shproxy: 代理映射配置
            services: 服务列表
        """        
        # 收集所有需要替换的 idref
        target_idrefs = {ref.idref for ref in shproxy.proxycompref}
        inst_elements.id = shproxy.id  # 使用 shproxy.id 作为新 id
        inst_elements.name = shproxy.name  # 使用 shproxy 的名称
        inst_elements.qualifier = shproxy.qual  # 使用 shproxy 的限定符
        inst_elements.description = shproxy.desc  # 使用 shproxy 的描述
        # inst_elements.must = shproxy.must  # 使用 shproxy 的 must 属性
        inst_elements.spec = shproxy.dest  # 使用 shproxy 的 dest 作为 spec
        
        # 遍历服务，替换匹配的元素
        for service in services:
            for msg in [service.request, service.positive_responses, service.negative_responses]:
                if msg is None:
                    continue
                for i, elem in enumerate(msg.elements):
                    if elem.id in target_idrefs:
                        msg.elements[i] = inst_elements
                        self._logger.debug(
                            f"代理映射替换: 原id={elem.id} -> 新元素id={shproxy.id}, "
                            f"来源={shproxy.dest}"
                        )