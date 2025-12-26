import numpy as np
from poincare import Variable
from poincare.types import Initial
from pytest import mark

from . import (
    Compartment,
    Constant,
    MassAction,
    Parameter,
    RateLaw,
    Simulator,
    Species,
    assign,
    initial,
)


def non_instance(model):
    return model


def instance(model):
    return model()


def check_species(
    x: Species,
    *,
    initial: Initial,
    parent: Compartment | type[Compartment],
):
    assert isinstance(x, Species)
    assert x.initial == initial
    assert x.parent is parent


def test_single_species():
    class Model(Compartment):
        x: Species = initial(default=0)

    model = Model
    check_species(model.x, initial=0, parent=model)
    model = Model()
    check_species(model.x, initial=0, parent=model)
    model = Model(x=1)
    check_species(model.x, initial=1, parent=model)


def test_yield_variables():
    class Model(Compartment):
        x: Species = initial(default=0)

    assert set(Model._yield(Species)) == {Model.x}
    assert set(Model._yield(Variable)) == {Model.x}


@mark.parametrize("f", [non_instance, instance])
def test_reaction(f):
    class Model(Compartment):
        x: Species = initial(default=0)
        c: Constant = assign(default=0, constant=True)
        eq1 = RateLaw(reactants=[x], products=[], rate_law=c)
        eq2 = RateLaw(reactants=[], products=[x], rate_law=c)
        eq3 = RateLaw(reactants=[2 * x], products=[3 * x], rate_law=c)

    model: Model = f(Model)
    assert model.x.equation_order == 1
    assert set(model.eq1.equations) == {model.x.derive() << -1 * model.c}
    assert set(model.eq2.equations) == {model.x.derive() << 1 * model.c}
    assert set(model.eq3.equations) == {model.x.derive() << 1 * model.c}


@mark.parametrize("f", [non_instance, instance])
def test_mass_action(f):
    class Model(Compartment):
        x: Species = initial(default=0)
        c: Constant = assign(default=0, constant=True)
        eq1 = MassAction(reactants=[x], products=[], rate=c)
        eq2 = MassAction(reactants=[], products=[x], rate=c)
        eq3 = MassAction(reactants=[2 * x], products=[3 * x], rate=c)

    model: Model = f(Model)
    assert model.x.equation_order == 1
    assert set(model.eq1.equations) == {
        model.x.derive() << -1 * (model.c * (model.x**1))
    }
    assert set(model.eq2.equations) == {model.x.derive() << 1 * model.c}
    assert set(model.eq3.equations) == {
        model.x.derive() << 1 * (model.c * (model.x**2))
    }


def test_duplicate_species():
    class Duplicate(Compartment):
        x: Species = initial(default=1)
        eq = MassAction(reactants=[x, x], products=[], rate=1)

    class Double(Compartment):
        x: Species = initial(default=1)
        eq = MassAction(reactants=[2 * x], products=[], rate=1)

    times = np.linspace(0, 1, 10)
    duplicate = Simulator(Duplicate).solve(save_at=times)
    double = Simulator(Double).solve(save_at=times)
    assert np.allclose(duplicate, double)


def test_simulator():
    class Model(Compartment):
        x: Species = initial(default=1)
        k: Parameter = assign(default=1)
        eq = MassAction(reactants=[x], products=[], rate=k)

    sim = Simulator(Model)
    assert set(sim.compiled.variables) == {Model.x}
    assert set(sim.compiled.parameters) == {Model.k}
    assert sim.compiled.mapper == {Model.x: 1, Model.k: 1}
    assert set(sim.transform.output) == {"x"}

    times = np.linspace(0, 1, 10)
    result = sim.solve(save_at=times)
    assert np.allclose(result["x"], np.exp(-times), rtol=1e-3, atol=1e-3)

    assert sim.create_problem({Model.x: 2}).y[0] == 2
    assert sim.create_problem({Model.x: 2}).y[0] == 2


def test_transform():
    class Model(Compartment):
        x: Species = initial(default=1)
        k: Parameter = assign(default=1)
        eq = MassAction(reactants=[x], products=[], rate=k)

    times = np.linspace(0, 1, 10)

    result = Simulator(Model).solve(save_at=times)
    result2 = Simulator(Model, transform={"double": 2 * Model.x}).solve(save_at=times)

    assert np.allclose(result2["double"], 2 * result["x"])
