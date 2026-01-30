from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

class BaseParser(ABC):
    """解析器基类：实现 match/parse 即可接入工厂"""
    priority: int = 0   # 用于冲突时排序，数值越大优先级越高

    def __init_subclass__(cls, **kwargs):
        """在子类定义阶段校验是否覆写关键方法"""
        super().__init_subclass__(**kwargs)
        if cls is BaseParser:
            return
        missing = []
        if cls.match is BaseParser.match:
            missing.append("match")
        if cls.parse is BaseParser.parse:
            missing.append("parse")
        if missing:
            raise TypeError(f"{cls.__name__} 必须实现方法: {', '.join(missing)}")

    @abstractmethod
    def match(self, data: Any) -> bool:
        """判断该解析器是否适用于当前数据"""
        pass

    @abstractmethod
    def parse(self, raw_obj: Any, raw_data_map: Dict[str, Any], strict: bool = True, get_data_from_id: Optional[Callable[[str], Any]] = None) -> Any:
        """执行解析逻辑

        Args:
            raw_obj: 待解析的原始对象
            raw_data_map: 包含所有原始数据的字典，因为部分数据可能需要直接使用原始数据，不需要解析
            get_data_from_id: 根据 ID 获取解析后数据的回调函数
        """
        pass