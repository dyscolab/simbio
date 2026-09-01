from symbolite import Real
from symbolite import translate
from typing import Any

class MathMLSpecialSymbol(Real):
    pass


class MathMLSymbol(Real):
    pass


@translate.register(MathMLSymbol)
def translate_MathMLSymbol(obj: MathMLSymbol, libsl: types.ModuleType) -> Any:
    return translate(Real(obj.__symbolite_info__.value), libsl)

@translate.register(MathMLSpecialSymbol)
def translate_MathMLSymbol(obj: MathMLSpecialSymbol, libsl: types.ModuleType) -> Any:
    return translate(Real(obj.__symbolite_info__.value), libsl)