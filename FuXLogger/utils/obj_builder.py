from dataclasses import is_dataclass, fields, Field
from typing import Type, TypeVar, get_args, get_origin, Optional, Any, Dict, Self
import inspect
from dataclasses import dataclass
from ..exceptions import ObjectBuildException

T = TypeVar('T')

def get_api_name(field: Field) -> str:
    """ 获取字段的API名称 """
    return field.metadata.get('api_name', field.name)

def build_obj(data: Dict[str, Any], obj: Type[T], type_cast: bool = False, verbose: bool = False) -> T:
    """
    根据data中的数据构建obj对象
    - data: 字典类型，包含obj对象的属性值
    - obj: 类类型，需要构建的对象类型
    - type_cast: bool类型，是否进行类型转换，默认False
    - verbose: bool类型，是否输出详细的构建信息，默认False
    - 返回值：obj对象
    - 异常：ObjectBuildException
    """
    if not is_dataclass(obj):
        raise ObjectBuildException(f"{obj} is not a dataclass")

    obj_fields = {get_api_name(field): field for field in fields(obj)}
    obj_data = {}
    
    if verbose:
        print(f"============  class  {obj.__name__} =============")
        print("properties:")
    
    for api_name, field in obj_fields.items():
        if api_name in data:
            field_value = data[api_name]
            origin_type = get_origin(field.type)
            
            if is_dataclass(field.type):
                obj_data[field.name] = build_obj(field_value, field.type, type_cast, verbose)  # 递归调用 # type: ignore
            elif origin_type is list:
                inner_type = get_args(field.type)[0]
                if is_dataclass(inner_type):
                    obj_data[field.name] = [build_obj(item, inner_type, type_cast, verbose) for item in field_value]  # 递归调用 # type: ignore
                else:
                    obj_data[field.name] = field_value
            elif origin_type is Optional:
                inner_type = get_args(field.type)[0]
                if field_value is not None and is_dataclass(inner_type):
                    obj_data[field.name] = build_obj(field_value, inner_type, type_cast, verbose)  # 递归调用 # type: ignore
                else:
                    obj_data[field.name] = field_value
            else:
                if type_cast:  # 类型转换部分
                    try:
                        # 转换类型
                        obj_data[field.name] = field.type(field_value)  # type: ignore
                    except (ValueError, TypeError):
                        # 如果转换失败，则保持原值
                        obj_data[field.name] = field_value
                else:
                    obj_data[field.name] = field_value
            
            if verbose:
                print(f"    build {field.name}, type {field.type.__name__}, value={obj_data[field.name]}")  # type: ignore
        else:
            # 支持默认值
            if field.default is not None:
                obj_data[field.name] = field.default
            else:
                obj_data[field.name] = None
    
    if verbose:
        print("methods:")
        for method_name in dir(obj):
            if callable(getattr(obj, method_name)) and not method_name.startswith("__"):
                method = getattr(obj, method_name)
                print(f"    def {method_name}({', '.join([param.name for param in inspect.signature(method).parameters.values()])}) -> {method.__annotations__.get('return', 'None')}: ...")
        print("============  end  =============")
    
    return obj(**obj_data)


# example usage
if __name__ == '__main__':
    @dataclass
    class A:
        a: int
        b: str
        c: Optional[Self] = None

        def get_something(self) -> str:
            return "something"
    
    data = {
        "a": 1,
        "b": "hello",
        "c": {
            "a": 2,
            "b": "world"
        }
    }
    
    obj = build_obj(data, A, verbose=True)
    print(obj)