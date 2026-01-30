"""
CDD 解析器自定义异常模块

异常层级设计:
    CddException (基类)
    ├── CddParseError (解析错误基类)
    │   ├── DuplicateIdError (重复ID错误)
    │   ├── IdNotFoundError (ID未找到错误)
    │   ├── ParserNotFoundError (解析器未找到错误)
    │   └── ParserExecutionError (解析器执行错误)
    ├── CddValidationError (验证错误基类)
    │   ├── RequiredFieldMissingError (必填字段缺失)
    │   └── InvalidFieldValueError (字段值无效)
    └── CddFileError (文件操作错误)
        ├── FileNotFoundError (文件未找到)
        └── FileFormatError (文件格式错误)
"""

from typing import Any, List, Optional, Tuple
import traceback
import sys


# ============ 错误格式化工具 ============

class ErrorFormatter:
    """
    错误格式化工具，用于生成清晰美观的错误报告
    """
    
    # ANSI 颜色代码（用于终端彩色输出）
    COLORS = {
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "green": "\033[92m",
        "gray": "\033[90m",
        "bold": "\033[1m",
        "reset": "\033[0m",
    }
    
    def __init__(self, use_color: bool = True):
        """
        初始化格式化器
        
        Args:
            use_color: 是否使用颜色（在不支持 ANSI 的终端中设为 False）
        """
        self.use_color = use_color and self._supports_color()
    
    @staticmethod
    def _supports_color() -> bool:
        """检测终端是否支持颜色"""
        if sys.platform == "win32":
            # Windows 10+ 默认支持，但需要检测
            try:
                import os
                return os.environ.get("TERM") or "ANSICON" in os.environ or hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
            except Exception:
                return False
        return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    
    def _color(self, text: str, color: str) -> str:
        """给文本添加颜色"""
        if not self.use_color:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"
    
    def format_exception(self, exc: Exception, show_traceback: bool = False) -> str:
        """
        格式化异常为清晰的错误报告
        
        Args:
            exc: 要格式化的异常
            show_traceback: 是否显示详细堆栈（调试用）
            
        Returns:
            格式化后的错误报告字符串
        """
        lines = []
        
        # 标题
        lines.append("")
        lines.append(self._color("═" * 70, "red"))
        lines.append(self._color("  ❌ CDD 解析错误", "bold"))
        lines.append(self._color("═" * 70, "red"))
        lines.append("")
        
        # 提取异常链
        error_chain = self._extract_error_chain(exc)
        
        # 根错误（最内层的原始错误）
        root_error = error_chain[-1] if error_chain else (type(exc).__name__, str(exc), None, None)
        
        lines.append(self._color("【根本原因】", "yellow"))
        lines.append(f"  类型: {self._color(root_error[0], 'cyan')}")
        lines.append(f"  信息: {root_error[1]}")
        if root_error[2]:  # 有位置信息
            lines.append(f"  位置: {self._color(root_error[2], 'gray')}")
        lines.append("")
        
        # 调用链（从外到内）
        if len(error_chain) > 1:
            lines.append(self._color("【调用链路】", "yellow"))
            for i, (err_type, err_msg, location, obj_id) in enumerate(error_chain[:-1]):
                prefix = "  └─► " if i == len(error_chain) - 2 else "  ├─► "
                indent = "      " if i == len(error_chain) - 2 else "  │   "
                
                # 显示异常类型和对象ID
                if obj_id:
                    lines.append(f"{prefix}{self._color(err_type, 'cyan')} (对象ID: {obj_id})")
                else:
                    lines.append(f"{prefix}{self._color(err_type, 'cyan')}")
                
                # 显示位置信息（完整路径）
                if location:
                    lines.append(f"{indent}位置: {self._color(location, 'gray')}")
            lines.append("")
        
        # 建议
        lines.append(self._color("【可能的解决方案】", "green"))
        suggestions = self._get_suggestions(error_chain)
        for suggestion in suggestions:
            lines.append(f"  • {suggestion}")
        lines.append("")
        
        # 详细堆栈（可选）
        if show_traceback:
            lines.append(self._color("【详细堆栈】", "gray"))
            tb_lines = traceback.format_exception(type(exc), exc, exc.__traceback__)
            for line in tb_lines:
                lines.append(self._color(f"  {line.rstrip()}", "gray"))
            lines.append("")
        
        lines.append(self._color("═" * 70, "red"))
        lines.append("")
        
        return "\n".join(lines)
    
    def _extract_error_chain(self, exc: Exception) -> List[Tuple[str, str, Optional[str], Optional[str]]]:
        """
        提取异常链信息
        
        Returns:
            列表，每项为 (异常类型名, 异常信息, 位置信息, 对象ID)
        """
        chain = []
        current = exc
        seen = set()  # 防止循环
        
        while current is not None and id(current) not in seen:
            seen.add(id(current))
            
            err_type = type(current).__name__
            err_msg = str(current)
            location = None
            obj_id = None
            
            # 提取对象 ID（如果是我们的自定义异常）
            if hasattr(current, 'obj_id'):
                obj_id = getattr(current, 'obj_id', None)
            
            # 提取位置信息
            # 对于 ParserExecutionError，我们需要找到实际调用解析器的位置
            # 而不是 raise 语句的位置
            if current.__traceback__:
                tb = traceback.extract_tb(current.__traceback__)
                if tb:
                    # 尝试找到有意义的调用位置
                    # 优先查找项目中的解析器文件（*_parser.py），跳过框架代码
                    meaningful_frame = None
                    for frame in reversed(tb):
                        filename_lower = frame.filename.lower()
                        # 跳过以下位置：
                        # 1. parser_factory.py 和 cdd_parser.py（异常传播的中间层）
                        # 2. logging_decorator.py（装饰器包装函数）
                        # 3. site-packages（第三方库）
                        # 4. Python 标准库
                        if ('parser_factory.py' in filename_lower or 
                            'cdd_parser.py' in filename_lower or
                            'logging_decorator.py' in filename_lower or
                            'site-packages' in filename_lower or
                            '\\lib\\' in filename_lower.replace('/', '\\')):
                            continue
                        meaningful_frame = frame
                        break
                    
                    # 如果没找到项目代码，尝试找 cdd 目录下的代码
                    if meaningful_frame is None:
                        for frame in reversed(tb):
                            if 'cdd' in frame.filename.lower() and 'site-packages' not in frame.filename.lower():
                                meaningful_frame = frame
                                break
                    
                    # 最后使用最后一帧
                    if meaningful_frame is None:
                        meaningful_frame = tb[-1]
                    
                    location = f"{meaningful_frame.filename}:{meaningful_frame.lineno} in {meaningful_frame.name}"
            
            chain.append((err_type, err_msg, location, obj_id))
            
            # 向下查找：先看 __cause__，再看 original_error 属性
            if current.__cause__ is not None:
                current = current.__cause__
            elif hasattr(current, 'original_error') and current.original_error is not None:
                current = current.original_error
            else:
                current = None
        
        return chain
    
    def _get_suggestions(self, error_chain: List[Tuple[str, str, Optional[str], Optional[str]]]) -> List[str]:
        """根据错误类型生成建议"""
        suggestions = []
        
        if not error_chain:
            return ["检查输入数据是否正确"]
        
        root_type, root_msg, _, _ = error_chain[-1]
        
        if "AttributeError" in root_type:
            if "'NoneType'" in root_msg:
                attr_name = root_msg.split("'")[-2] if "'" in root_msg else "未知"
                suggestions.append(f"检查对象是否为 None，属性 '{attr_name}' 不存在")
                suggestions.append("确认 CDD 文件中该字段是否已定义")
                suggestions.append("在解析器中添加 None 值检查")
        elif "KeyError" in root_type or "IdNotFoundError" in root_type:
            suggestions.append("确认引用的 ID 在 CDD 文件中存在")
            suggestions.append("检查 ID 拼写是否正确")
        elif "DuplicateIdError" in root_type:
            suggestions.append("检查 CDD 文件中是否存在重复的 ID 定义")
            suggestions.append("考虑使用 strict=False 模式跳过重复项")
        elif "ParserNotFoundError" in root_type:
            suggestions.append("为该类型的对象实现对应的解析器")
            suggestions.append("检查解析器的 match() 方法是否正确")
        else:
            suggestions.append("检查 CDD 文件格式是否正确")
            suggestions.append("尝试使用 strict=False 模式查看更多信息")
        
        return suggestions


# ============ 异常基类 ============

class CddException(Exception):
    """CDD 解析器所有异常的基类"""
    
    def __init__(self, message: str, details: Optional[Any] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)
    
    def __str__(self) -> str:
        # 简洁的单行表示
        return self.message
    
    def detailed_str(self) -> str:
        """返回包含详情的完整字符串"""
        if self.details:
            return f"{self.message} | 详情: {self.details}"
        return self.message
    
    def format_error(self, show_traceback: bool = False, use_color: bool = True) -> str:
        """格式化为美观的错误报告"""
        formatter = ErrorFormatter(use_color=use_color)
        return formatter.format_exception(self, show_traceback=show_traceback)


# ============ 解析错误 ============

class CddParseError(CddException):
    """解析过程中发生的错误基类"""
    pass


class DuplicateIdError(CddParseError):
    """发现重复的 ID"""
    
    def __init__(self, obj_id: str, existing_obj: Any = None, new_obj: Any = None):
        self.obj_id = obj_id
        self.existing_obj = existing_obj
        self.new_obj = new_obj
        existing_type = type(existing_obj).__name__ if existing_obj else "Unknown"
        new_type = type(new_obj).__name__ if new_obj else "Unknown"
        message = f"发现重复ID: {obj_id} (已存在: {existing_type}, 新对象: {new_type})"
        super().__init__(message)


class IdNotFoundError(CddParseError):
    """引用的 ID 在索引中未找到"""
    
    def __init__(self, ref_id: str, context: Optional[str] = None):
        self.ref_id = ref_id
        self.obj_id = ref_id  # 兼容错误链提取
        self.context = context
        message = f"引用ID未找到: {ref_id}"
        if context:
            message += f" ({context})"
        super().__init__(message)


class ParserNotFoundError(CddParseError):
    """找不到合适的解析器处理该对象"""
    
    def __init__(self, obj_type: str, obj_id: Optional[str] = None):
        self.obj_type = obj_type
        self.obj_id = obj_id
        message = f"无法找到解析器处理类型: {obj_type}"
        if obj_id:
            message += f" (ID: {obj_id})"
        super().__init__(message)


class ParserExecutionError(CddParseError):
    """解析器执行过程中发生错误"""
    
    def __init__(
        self, 
        parser_name: str, 
        obj_id: Optional[str] = None, 
        original_error: Optional[Exception] = None
    ):
        self.parser_name = parser_name
        self.obj_id = obj_id
        self.original_error = original_error
        message = f"解析器 {parser_name} 执行失败"
        if obj_id:
            message += f" (对象ID: {obj_id})"
        super().__init__(message)


# ============ 验证错误 ============

class CddValidationError(CddException):
    """数据验证错误基类"""
    pass


class RequiredFieldMissingError(CddValidationError):
    """必填字段缺失"""
    
    def __init__(self, field_name: str, obj_type: str, obj_id: Optional[str] = None):
        self.field_name = field_name
        self.obj_type = obj_type
        self.obj_id = obj_id
        message = f"对象 {obj_type} 缺少必填字段: {field_name}"
        details = {"obj_id": obj_id} if obj_id else None
        super().__init__(message, details)


class InvalidFieldValueError(CddValidationError):
    """字段值无效"""
    
    def __init__(
        self, 
        field_name: str, 
        field_value: Any, 
        expected: str,
        obj_type: Optional[str] = None
    ):
        self.field_name = field_name
        self.field_value = field_value
        self.expected = expected
        message = f"字段 {field_name} 值无效: {field_value}"
        details = {
            "expected": expected,
            "actual_type": type(field_value).__name__,
            "obj_type": obj_type,
        }
        super().__init__(message, details)


# ============ 文件错误 ============

class CddFileError(CddException):
    """文件操作错误基类"""
    pass


class CddFileNotFoundError(CddFileError):
    """CDD 文件未找到"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        message = f"CDD 文件未找到: {file_path}"
        super().__init__(message)


class CddFileFormatError(CddFileError):
    """CDD 文件格式错误"""
    
    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        message = f"CDD 文件格式错误: {file_path}"
        super().__init__(message, reason)
