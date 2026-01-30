import logging as _logging
from functools import wraps
from typing import Callable, Optional, Type, TypeVar, Union

T = TypeVar("T")


def logging(
    cls: Optional[Type[T]] = None,
    *,
    level: int = _logging.INFO,
    fmt: str = "%(asctime)s | %(levelname)s | %(pathname)s:%(lineno)d | %(message)s",
    datefmt: str = "%Y-%m-%d %H:%M:%S",
) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    """类装饰器：注入 _logger 并统一日志格式。"""

    def decorator(target_cls: Type[T]) -> Type[T]:
        original_init = getattr(target_cls, "__init__", None)
        
        # 检查 original_init 是否是从 object 继承的默认 __init__
        # 如果是，则视为 None 处理
        if original_init is object.__init__:
            original_init = None

        def new_init(self, *args, **kwargs):
            # 仅设置 logger 实例
            self._logger = _logging.getLogger(
                f"{target_cls.__module__}.{target_cls.__name__}"
            )
            # 如果需要，可以单独为这个 logger 设置 level，但不应干涉 root logger
            # self._logger.setLevel(level) 
            
            if original_init is not None:
                original_init(self, *args, **kwargs)

        # 仅当 original_init 存在且不为 None 时才使用 @wraps
        if original_init is not None:
            new_init = wraps(original_init)(new_init)
        else:
            new_init.__name__ = "__init__"
            new_init.__qualname__ = f"{target_cls.__qualname__}.__init__"

        target_cls.__init__ = new_init
        return target_cls

    if cls is not None:
        return decorator(cls)
    return decorator
