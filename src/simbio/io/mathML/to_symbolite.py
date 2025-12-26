from __future__ import annotations

from functools import partial, reduce
from typing import Iterator, Protocol

from symbolite.abstract import real

from .symbol import MathMLSpecialSymbol, MathMLSymbol


class Element(Protocol):
    @property
    def tag(self) -> str: ...

    @property
    def attrib(self) -> dict[str, str]: ...

    @property
    def text(self) -> str: ...

    def __iter__(self) -> Iterator[Element]: ...


def star_reduce(func, *args):
    return reduce(func, args)


tags = {
    "cn": MathMLSymbol,
    "ci": MathMLSpecialSymbol,
    "csymbol": MathMLSpecialSymbol,
    "sep": NotImplemented,
    "apply": NotImplemented,
    "piecewise": NotImplemented,
    "piece": NotImplemented,
    "otherwise": NotImplemented,
    "lambda": NotImplemented,
    "eq": real.eq,
    "neq": real.ne,
    "gt": real.gt,
    "lt": real.lt,
    "geq": real.ge,
    "leq": real.le,
    "plus": partial(star_reduce, real.add),
    "minus": partial(star_reduce, real.sub),
    "times": partial(star_reduce, real.mul),
    "divide": partial(star_reduce, real.truediv),
    "power": real.pow,
    "root": NotImplemented,
    "abs": real.abs,
    "exp": real.exp,
    "ln": real.log,
    "log": real.log10,
    "floor": real.floor,
    "ceiling": real.ceil,
    "factorial": real.factorial,
    "quotient": NotImplemented,
    "max": NotImplemented,
    "min": NotImplemented,
    "rem": real.mod,
    "and": partial(star_reduce, real.and_),
    "or": partial(star_reduce, real.or_),
    "xor": real.xor,
    "not": real.invert,
    "implies": NotImplemented,
    "degree": NotImplemented,
    "bvar": NotImplemented,
    "logbase": NotImplemented,
    "sin": real.sin,
    "cos": real.cos,
    "tan": real.tan,
    "sec": NotImplemented,
    "csc": NotImplemented,
    "cot": NotImplemented,
    "sinh": real.sinh,
    "cosh": real.cosh,
    "tanh": real.tanh,
    "sech": NotImplemented,
    "csch": NotImplemented,
    "coth": NotImplemented,
    "arcsin": real.asin,
    "arccos": real.acos,
    "arctan": real.atan,
    "arcsec": NotImplemented,
    "arccsc": NotImplemented,
    "arccot": NotImplemented,
    "arcsinh": real.asinh,
    "arccosh": real.acosh,
    "arctanh": real.atanh,
    "arcsech": NotImplemented,
    "arccsch": NotImplemented,
    "arccoth": NotImplemented,
    "true": True,
    "false": False,
    "notanumber": real.nan,
    "pi": real.pi,
    "infinity": real.inf,
    "exponentiale": real.e,
    "semantics": NotImplemented,
    "annotation": NotImplemented,
    "annotation-xml": NotImplemented,
    "math": lambda x: x,
}

ns_map = {"http://www.w3.org/1998/Math/MathML": tags}


def from_element(element: Element) -> Real:
    result = parse(element)
    if isinstance(result, list) and len(result) == 1:
        return result[0]
    raise RuntimeError("unexpected result when parsing mathML")


def _namespace_and_tag(x: str) -> tuple[str, str]:
    if x.startswith("{"):
        ns, _, tag = x[1:].partition("}")
        return ns, tag
    else:
        return "", x


def parse(element: Element):
    ns, tag = _namespace_and_tag(element.tag)
    cls = ns_map[ns][tag]

    if tag == "apply":
        func, *children = (parse(child) for child in element)
        return func(*children)

    children = [parse(child) for child in element]
    if len(children) > 0:
        return children
    elif (text := element.text) is not None:
        return cls(text.strip())
    else:
        return cls
