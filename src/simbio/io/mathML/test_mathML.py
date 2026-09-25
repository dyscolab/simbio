from pytest import mark
from symbolite.abstract import real

from . import mathMLImporter, to_mathML
from .symbol import MathMLSymbol as Symbol

x, y = map(Symbol, ["x", "y"])


@mark.parametrize(
    "expr",
    [
        1,
        x,
        x * y,
        x + y,
        x * 2,
        2 * x,
        2 * x + y,
        x**2,
        x**0.5,
        real.cos(x),
        real.sqrt(x),
        x < 1,
        x < y,
        ~x,
    ],
)
def test_mathML_roundtrip(expr: Symbol):
    node = to_mathML(expr)
    expr2 = mathMLImporter().convert(node)
    assert expr2 == expr


def test_compile_function():
    import libsbml
    from pytest import raises

    ast = libsbml.parseL3Formula("lambda(a, b, a * b + 2)")
    importer = mathMLImporter()
    func = importer.compile_function("my_func", ast)

    assert func(x, y) == x * y + 2
    assert func(a=x, b=y) == x * y + 2
    assert func(b=y, a=x) == x * y + 2

    with raises(TypeError):
        func(x)
    with raises(TypeError):
        func(x, y, x)


def test_sbml_function_definition():
    from ..sbml import loads

    sbml = """<?xml version="1.0" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
  <model id="test_func_model" name="test_func_model">
    <listOfFunctionDefinitions>
      <functionDefinition id="rate_func">
        <math xmlns="http://www.w3.org/1998/Math/MathML">
          <lambda>
            <bvar><ci> k </ci></bvar>
            <bvar><ci> s </ci></bvar>
            <apply>
              <times/>
              <ci> k </ci>
              <ci> s </ci>
            </apply>
          </lambda>
        </math>
      </functionDefinition>
    </listOfFunctionDefinitions>
    <listOfCompartments>
      <compartment id="c" spatialDimensions="3" size="1" constant="true"/>
    </listOfCompartments>
    <listOfSpecies>
      <species id="S1" compartment="c" initialConcentration="1.0" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
      <species id="S2" compartment="c" initialConcentration="0.0" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
    </listOfSpecies>
    <listOfParameters>
      <parameter id="k1" value="0.5" constant="true"/>
    </listOfParameters>
    <listOfReactions>
      <reaction id="r1" reversible="false">
        <listOfReactants>
          <speciesReference species="S1" constant="true"/>
        </listOfReactants>
        <listOfProducts>
          <speciesReference species="S2" constant="true"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <ci> rate_func </ci>
              <ci> k1 </ci>
              <ci> S1 </ci>
            </apply>
          </math>
        </kineticLaw>
      </reaction>
    </listOfReactions>
  </model>
</sbml>"""

    model = loads(sbml)
    assert hasattr(model, "S1")
    assert hasattr(model, "S2")
    assert hasattr(model, "r1")

