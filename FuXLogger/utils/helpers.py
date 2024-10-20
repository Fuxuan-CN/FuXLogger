import warnings
from typing import Callable, Any, Optional, Type , Union
import inspect

class Deprecated:
    """
    ### Decorator for deprecated functions and classes.
    - 对弃用函数和类标记的装饰器
    
    ### three methods to how to use this decorators
    ### 此装饰器使用的三种方法
    
    - 1. 指定原因(input reason for deprecated functions)
    
    ```
    @Deprecated("this is a test")
    def test1():
        print("test1")
    ```
    
    - 2. 指定移除版本号(input deprecated version)
    
    ```
    @Deprecated("test", d_version="0.1.0", remove=True)
    def test2():
        print("test2")
    ```
    
    - 3. 指定新函数名(input new function name)
    
    ```
    @Deprecated("test", newFuncName="test4")
    def test3():
        print("test3")
    ```
    """

    def __init__(self, 
                 reason: str = "no reasons",
                 d_version: Optional[str] = None,
                 newName: Optional[str] = None,
                 remove: bool = False
                ) -> None:
        self.reason = reason
        self.d_version = d_version
        self.newName = newName
        self.remove = remove

    def __call__(self, obj: Union[Callable[..., Any], Type]) -> Union[Callable[..., Any], Type]:
        """
        Handle function or class decoration.
        """
        if inspect.isclass(obj):
            return self._decorate_class(obj)
        elif inspect.isfunction(obj):
            return self._decorate_function(obj)
        else:
            raise TypeError("Deprecated can only be used on functions or classes.")

    def _decorate_function(self, func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorates a function.
        """
        func_signature = inspect.signature(func)

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not func.__name__ == "new_init": 
                self._warn("function", func.__name__)
            return func(*args, **kwargs)

        wrapper.__signature__ = func_signature
        return wrapper

    def _decorate_class(self, cls: Type) -> Type:
        """
        Decorates a class.
        """
        original_init = cls.__init__

        def new_init(instance, *args: Any, **kwargs: Any) -> None:
            self._warn("class", cls.__name__)
            original_init(instance, *args, **kwargs)

        cls.__init__ = new_init

        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value):
                setattr(cls, attr_name, self._decorate_function(attr_value))
        
        return cls

    def _warn(self, is_what: str, name: str) -> None:
        """
        Issues the warning based on the configuration.
        """
        formatted_reason = f"Deprecated as {self.reason}, Deprecated {is_what}: {name}"
        if self.d_version:
            formatted_reason += f", will be removed in version {self.d_version}"

        if self.remove:
            stacklevel = 3 if is_what == "function" else 4
            warnings.warn(f"{formatted_reason}.", DeprecationWarning, stacklevel=stacklevel)
        elif self.newName:
            stacklevel = 3 if is_what == "function" else 4
            warnings.warn(f"{formatted_reason}, use {self.newName} instead.", FutureWarning, stacklevel=stacklevel)
        else:
            stacklevel = 3 if is_what == "function" else 4
            warnings.warn(formatted_reason, DeprecationWarning, stacklevel=stacklevel)


if __name__ == "__main__":
    
    @Deprecated("this is a test")
    class Test: ...

    @Deprecated("this is a test")
    def test():
        print("test")

    test()
    testClass = Test()