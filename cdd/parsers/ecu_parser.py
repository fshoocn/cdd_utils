import json
from dataclasses import asdict
from typing import Any, Callable, Dict, Optional

from ..models.candela import Ecu, Name, Tuv
from .base_parser import BaseParser
from ..models.cdd_model import DiagnosticGroup, DiagnosticInstance, EcuModel

from ..utils.logging import logging

@logging
class EcuParser(BaseParser):
    priority = 90  # 优先级较高

    def match(self, raw_obj: Any) -> bool:
        # raw_obj对象是否为 ECU
        return isinstance(raw_obj, Ecu)


    def parse(self, raw_obj: Ecu, raw_data_map: Dict[str, Any], strict: bool = True, get_data_from_id: Optional[Callable[[str], Any]] = None) -> EcuModel:
        name = raw_obj.name if raw_obj.name is not None else Name(tuv=[Tuv(lang="en-US", value="Unnamed ECU"),Tuv(lang="zh-CN", value="未命名 ECU")])
        diag_list: list[DiagnosticInstance | DiagnosticGroup] = []
        for diag in raw_obj.var.diag:
            diag_list.append(get_data_from_id(diag.id))
            self._logger.debug(f"diag: {json.dumps(asdict(diag_list[-1]), default=str, ensure_ascii=False, indent=2)}")
        # self._logger.debug(f"完成解析diag_list,内容: {json.dumps([asdict(d) for d in diag_list], default=str, ensure_ascii=False, indent=2)}")
        return EcuModel(
            id=raw_obj.id,
            name=name,
            qualifier=raw_obj.qual,
            diag_list=diag_list
        )