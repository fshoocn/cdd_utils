"""CDD V2 异常层级"""


class CddParseError(Exception):
    """CDD 解析过程中的通用异常"""
    pass


class TransformError(CddParseError):
    """转换器执行错误"""
    def __init__(self, transformer_name: str, obj_id: str, original_error: Exception = None):
        self.transformer_name = transformer_name
        self.obj_id = obj_id
        self.original_error = original_error
        msg = f"转换器 {transformer_name} 处理对象 {obj_id} 时失败"
        if original_error:
            msg += f": {original_error}"
        super().__init__(msg)


class CodecError(CddParseError):
    """编解码错误"""
    pass


class EncodeError(CodecError):
    """编码错误"""
    pass


class DecodeError(CodecError):
    """解码错误"""
    pass
