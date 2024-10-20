from typing import TypeVar, TYPE_CHECKING, TypeAlias
import sys

if TYPE_CHECKING:
    if sys.version_info >= (3, 12):
        # 在 Python 3.12 及以上版本中，使用 `type` 关键字
        type Message = str | bytes
    elif sys.version_info >= (3, 11):
        # 在 Python 3.11 及以上版本中，使用 `TypeAlias`
        Message: TypeAlias = str | bytes
    else:
        # 在 Python 3.10 及以下版本中，使用 TypeVar
        Message = TypeVar("Message", str, bytes)
else:
   # 在不进行类型检查时，定义一个通用的 Message TypeVar
   Message = TypeVar("Message", str, bytes)