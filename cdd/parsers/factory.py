
import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .base_parser import BaseParser
from ..utils.logging import logging
from ..utils.exceptions import ParserNotFoundError, ParserExecutionError

@logging
class ParserFactory:
    _instance = None
    # 类级缓存，避免重复扫描与重复实例化
    _parsers: Optional[List[BaseParser]] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化解析器工厂并加载解析器列表"""
        # 仅在首次实例化时发现解析器
        if ParserFactory._parsers is None:
            ParserFactory._parsers = []
            self._discover_parsers()
        self.parsers = ParserFactory._parsers

    def _discover_parsers(self):
        """扫描 parser 目录（包括子目录）并实例化可用解析器"""
        parser_path = Path(__file__).parent
        self._logger.debug(f"扫描解析器目录: {parser_path}")
        self._scan_parser_package(parser_path, "cdd.parsers")
        
        # 按优先级排序，数值越大越优先
        ParserFactory._parsers.sort(key=lambda p: p.priority, reverse=True)
        self._logger.info(f"已加载解析器: {[p.__class__.__name__ for p in ParserFactory._parsers]}")

    def _scan_parser_package(self, package_path: Path, package_prefix: str):
        """递归扫描指定包路径下的所有解析器模块
        
        Args:
            package_path: 包的文件系统路径
            package_prefix: 包的导入前缀（如 '.parser' 或 '.parser.comp_parser'）
        """
        for _, name, is_pkg in pkgutil.iter_modules([str(package_path)]):
            full_module_name = f"{package_prefix}.{name}"
            
            if is_pkg:
                # 递归扫描子包
                sub_path = package_path / name
                self._scan_parser_package(sub_path, full_module_name)
            else:
                # 扫描模块中的解析器类
                try:
                    module = importlib.import_module(full_module_name, package='cdd.parsers')
                    
                    for _, obj in inspect.getmembers(module, inspect.isclass):
                        # 只收集 BaseParser 的非抽象子类
                        if (issubclass(obj, BaseParser) and 
                            obj is not BaseParser and 
                            not obj.__abstractmethods__):
                            ParserFactory._parsers.append(obj())
                except Exception as e:
                    self._logger.warning(f"加载解析器模块失败: {full_module_name}. 错误信息: {e}")
                    continue
        
    def parse(self, raw_obj: Any, raw_data_map: Dict[str, Any],strict = False, get_data_from_id: Optional[Callable[[str], Any]] = None) -> Any:
        """寻找匹配的 Parser 并解析
        
        Args:
            raw_obj: 待解析的对象
            get_data_from_id: 根据 ID 获取解析后数据的回调函数
            
        Raises:
            ParserExecutionError: 解析器执行失败
            ParserNotFoundError: 找不到合适的解析器
        """
        parsing_errors: List[Exception] = []
        last_error: Optional[Exception] = None

        # 按优先级依次尝试解析器
        for parser in self.parsers:
            if parser.match(raw_obj):
                try:
                    self._logger.debug(f"使用解析器 {parser.__class__.__name__} 解析对象 ID: {getattr(raw_obj, 'id', None)} 类型: {type(raw_obj).__name__}")
                    return parser.parse(raw_obj, raw_data_map=raw_data_map, strict=strict, get_data_from_id=get_data_from_id)
                except Exception as e:
                    # 当前解析器失败，记录后继续尝试下一个解析器
                    # 不打印完整 traceback，只记录简洁信息
                    parsing_errors.append(e)
                    last_error = e
                    self._logger.debug(f"解析器 {parser.__class__.__name__} 解析失败: {e}，尝试下一个解析器")
                    continue

        # 循环结束仍未返回，说明没有解析器成功解析
        obj_type = type(raw_obj).__name__
        obj_id = getattr(raw_obj, 'id', None)
        
        if parsing_errors:
            # 这种情况属于找到了匹配的解析器，但是解析过程中出错了
            # 保留最后一个（通常是最相关的）原始异常，便于追踪根因
            if strict:
                raise ParserExecutionError(
                    parser_name=parsing_errors[-1].__class__.__name__ if last_error else "Unknown",
                    obj_id=obj_id,
                    original_error=last_error
                ) from last_error
        else:
            # 这种情况属于没有解析器 match 该对象
            self._logger.debug(f'无法找到合适的解析器来处理对象: {obj_type}')
            if strict:
                raise ParserNotFoundError(obj_type=obj_type, obj_id=obj_id)

        self._logger.warning(f"解析失败 ({obj_type}), 将返回 None.")
        return None