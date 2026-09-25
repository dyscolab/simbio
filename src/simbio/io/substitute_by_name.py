from functools import singledispatch
from typing import Any
from symbolite.core.value import Value, Name
from symbolite.core.symbolite_object import get_symbolite_info
from symbolite.core.call import Call

@singledispatch
def substitute_by_name(expr: Any, **mapper: Any) -> Any:
    return expr


@substitute_by_name.register(Value)
def call_substitute_by_name(expr: Value, **mapper: Any) -> Any:
    """Replace Value by values or objects, matching by name.

    If multiple mappers are provided,
        they will be used in order (using a ChainMap)

    If a given object is not found in the mappers,
        the same object will be returned.

    Parameters
    ----------
    **mapper
        keyword arguments connecting names to values.
    """

    value = get_symbolite_info(expr).value
    if isinstance(value, Name):
        return mapper.get(value.name, expr)
    return substitute_by_name(value, **mapper)


@substitute_by_name.register(Call)
def value_substitute_by_name(expr: Call, **mapper: Any) -> Any:
    """Replace symbols, functions, values, etc by others.

    If multiple mappers are provided,
        they will be used in order (using a ChainMap)

    If a given object is not found in the mappers,
        the same object will be returned.

    Parameters
    ----------
    mappers
        dictionary mapping source to destination objects.
    """
    info = get_symbolite_info(expr)

    func = mapper.get(str(info.func), info.func)
    args = tuple(substitute_by_name(arg, **mapper) for arg in info.args)
    kwargs = {k: substitute_by_name(arg, **mapper) for k, arg in info.kwargs_items}

    try:
        return func(*args, **kwargs)
    except Exception as ex:
        try:
            ex.add_note(f"While evaluating {func}(*{args}, **{kwargs}): {ex}")
        except AttributeError:
            pass
        raise ex
