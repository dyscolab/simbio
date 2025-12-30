import numpy as np
from poincare import Variable, System, Independent
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
from .core import Volume, concentration, amount, volume


def test_no_external_species_in_nested_comparment():
    class Nested(Compartment):
        V: Volume = volume(default=1)
        A: Species = amount(default=1)

        eq = RateLaw(reactants=[A], products=[2 * A], rate_law=1)

    try:

        class Model(Compartment):
            V: Volume = volume(default=1)
            A: Species = amount(default=1)

            nested = Nested(A=A)
            eq = RateLaw(reactants=[A], products=[2 * A], rate_law=1)
    except TypeError:
        assert True
        return
    assert False


def test_no_volume_in_compartment():
    try:

        class Model(Compartment):
            A: Species = amount(default=1)

            eq = RateLaw(reactants=[A], products=[2 * A], rate_law=1)
    except AttributeError:
        assert True
        return
    assert False


def test_more_than_one_volume_in_compartment():
    try:

        class Model(Compartment):
            V1: Volume = volume(default=1)
            V2: Volume = volume(default=1)
            A: Species = amount(default=1)

            eq = RateLaw(reactants=[A], products=[2 * A], rate_law=1)
    except AttributeError:
        assert True
        return
    assert False


def test_rate_law_with_amount():
    class Model(System):
        A: Variable = Variable(initial=1)
        B: Variable = Variable(initial=2)
        AB: Variable = Variable(initial=0)

        eq = RateLaw(reactants=[A, 2 * B], products=[AB], rate_law=1)

    sim1 = Simulator(Model)
    result_1 = sim1.solve(save_at=np.linspace(0, 10, 10))

    class VolumeModel(Compartment):
        V: Volume = volume(default=2)
        A: Species = amount(default=1)
        B: Species = amount(default=2)
        AB: Species = amount(default=0)

        eq = RateLaw(reactants=[A, 2 * B], products=[AB], rate_law=1)

    sim2 = Simulator(VolumeModel)
    result_2 = sim2.solve(save_at=np.linspace(0, 10, 10))[["A", "AB", "B"]]
    assert np.all(result_2 == result_1)


def test_rate_law_with_concentration():
    class Model(System):
        A: Variable = Variable(initial=1)
        B: Variable = Variable(initial=2)
        AB: Variable = Variable(initial=0)

        eq = RateLaw(reactants=[A, 2 * B], products=[AB], rate_law=1 / 2)

    sim1 = Simulator(Model)
    result_1 = sim1.solve(save_at=np.linspace(0, 10, 10))

    class VolumeModel(Compartment):
        V: Volume = volume(default=2)
        A: Species = concentration(default=1)
        B: Species = concentration(default=2)
        AB: Species = concentration(default=0)

        eq = RateLaw(reactants=[A, 2 * B], products=[AB], rate_law=1)

    sim2 = Simulator(VolumeModel)
    result_2 = sim2.solve(save_at=np.linspace(0, 10, 10))[["A", "AB", "B"]]
    assert np.all(result_2 == result_1)


def test_mixed_rate_law():
    class Model(System):
        A: Variable = Variable(initial=1)
        B: Variable = Variable(initial=2)
        AB: Variable = Variable(initial=0)

        eq1 = RateLaw(reactants=[A, 2 * B], products=[AB], rate_law=1 / 2)
        eq2 = AB.derive() << 1 / 2

    sim1 = Simulator(Model)
    result_1 = sim1.solve(save_at=np.linspace(0, 10, 10))

    class VolumeModel(Compartment):
        V: Volume = volume(default=2)
        A: Species = concentration(default=1)
        B: Species = concentration(default=2)
        AB: Species = amount(default=0)

        eq = RateLaw(reactants=[A, 2 * B], products=[AB], rate_law=1)

    sim2 = Simulator(VolumeModel)
    result_2 = sim2.solve(save_at=np.linspace(0, 10, 10))[["A", "AB", "B"]]
    assert np.all(result_2 == result_1)


def test_mass_action_with_amount():
    class Model(System):
        A: Variable = Variable(initial=1)
        B: Variable = Variable(initial=2)
        AB: Variable = Variable(initial=0)

        eq = RateLaw(
            reactants=[A, 2 * B], products=[AB], rate_law=(A / 2) * (B / 2) ** 2
        )

    sim1 = Simulator(Model)
    result_1 = sim1.solve(save_at=np.linspace(0, 10, 10))

    class VolumeModel(Compartment):
        V: Volume = volume(default=2)
        A: Species = amount(default=1)
        B: Species = amount(default=2)
        AB: Species = amount(default=0)

        eq = MassAction(reactants=[A, 2 * B], products=[AB], rate=1)

    sim2 = Simulator(VolumeModel)
    result_2 = sim2.solve(save_at=np.linspace(0, 10, 10))[["A", "AB", "B"]]
    assert np.all(result_2 == result_1)


def test_mass_action_with_concentration():
    class Model(System):
        A: Variable = Variable(initial=1)
        B: Variable = Variable(initial=2)
        AB: Variable = Variable(initial=0)

        eq = RateLaw(reactants=[A, 2 * B], products=[AB], rate_law=A * B**2 / 2)

    sim1 = Simulator(Model)
    result_1 = sim1.solve(save_at=np.linspace(0, 10, 10))

    class VolumeModel(Compartment):
        V: Volume = volume(default=2)
        A: Species = concentration(default=1)
        B: Species = concentration(default=2)
        AB: Species = concentration(default=0)

        eq = MassAction(reactants=[A, 2 * B], products=[AB], rate=1)

    sim2 = Simulator(VolumeModel)
    result_2 = sim2.solve(save_at=np.linspace(0, 10, 10))[["A", "AB", "B"]]
    assert np.all(result_2 == result_1)


def test_mixed_mass_action():
    class Model(Compartment):
        V: Volume = volume(default=2)
        A: Species = concentration(default=1)
        B: Species = amount(default=2)
        AB: Species = concentration(default=0)

        eq = RateLaw(reactants=[A, 2 * B], products=[AB], rate_law=A * (B / 2) ** 2)

    sim1 = Simulator(Model)
    result_1 = sim1.solve(save_at=np.linspace(0, 10, 10))

    class VolumeModel(Compartment):
        V: Volume = volume(default=2)
        A: Species = concentration(default=1)
        B: Species = amount(default=2)
        AB: Species = concentration(default=0)

        eq = MassAction(reactants=[A, 2 * B], products=[AB], rate=1)

    sim2 = Simulator(VolumeModel)
    result_2 = sim2.solve(save_at=np.linspace(0, 10, 10))
    assert np.all(result_2 == result_1)


def test_changing_volume():
    class Model(System):
        t: Independent = Independent()
        V: Parameter = assign(default=t**2 / 2 + 1)
        A: Variable = Variable(initial=1)
        B: Variable = Variable(initial=2)
        AB: Variable = Variable(initial=0)

        eq = RateLaw(reactants=[A, 2 * B], products=[AB], rate_law=A * B**2 / V)

    sim1 = Simulator(Model)
    result_1 = sim1.solve(save_at=np.linspace(0, 10, 10))

    class VolumeModel(Compartment):
        t: Independent = Independent()
        V: Volume = volume(default=1)
        A: Species = concentration(default=1)
        B: Species = concentration(default=2)
        AB: Species = concentration(default=0)

        eq = MassAction(reactants=[A, 2 * B], products=[AB], rate=1)
        vol_eq = V.derive() << t

    sim2 = Simulator(VolumeModel)
    result_2 = sim2.solve(save_at=np.linspace(0, 10, 10))
    calculated_volumes = np.linspace(0, 10, 10) ** 2 / 2 + 1
    volumes = np.asarray(result_2["V"])
    assert np.all(
        np.abs((result_1 - result_2[["A", "AB", "B"]]))
        <= (result_1 + result_2[["A", "AB", "B"]]) / 2 * 0.01
    )
    assert np.all(
        np.abs(calculated_volumes - volumes)
        <= (calculated_volumes + volumes) / 2 * 0.01
    )


def test_nested_compartments():
    class Nested(Compartment):
        V: Volume = volume(default=1)
        A: Species = amount(default=1)

        eq = RateLaw(reactants=[A], products=[2 * A], rate_law=1)

    class Model(Compartment):
        V: Volume = volume(default=1)
        A: Species = amount(default=1)

        nested = Nested()
        eq = RateLaw(reactants=[A], products=[2 * A], rate_law=1)

    sim = Simulator(Model)
    sim.solve(save_at=np.linspace(0, 10, 10))

    assert Model.A and Model.nested.A in sim.compiled.variables
    assert Model._volume == Model.V
    assert Model.nested._volume == Model.nested.V


# def check_species(
#     x: Species,
#     *,
#     initial: Initial,
#     parent: Compartment | type[Compartment],
# ):
#     assert isinstance(x, Species)
#     assert x.initial == initial
#     assert x.parent is parent


# def test_single_species():
#     class Model(Compartment):
#         x: Species = initial(default=0)

#     model = Model
#     check_species(model.x, initial=0, parent=model)
#     model = Model()
#     check_species(model.x, initial=0, parent=model)
#     model = Model(x=1)
#     check_species(model.x, initial=1, parent=model)


# def test_yield_variables():
#     class Model(Compartment):
#         x: Species = initial(default=0)

#     assert set(Model._yield(Species)) == {Model.x}
#     assert set(Model._yield(Variable)) == {Model.x}


# @mark.parametrize("f", [non_instance, instance])
# def test_reaction(f):
#     class Model(Compartment):
#         x: Species = initial(default=0)
#         c: Constant = assign(default=0, constant=True)
#         eq1 = RateLaw(reactants=[x], products=[], rate_law=c)
#         eq2 = RateLaw(reactants=[], products=[x], rate_law=c)
#         eq3 = RateLaw(reactants=[2 * x], products=[3 * x], rate_law=c)

#     model: Model = f(Model)
#     assert model.x.equation_order == 1
#     assert set(model.eq1.equations) == {model.x.derive() << -1 * model.c}
#     assert set(model.eq2.equations) == {model.x.derive() << 1 * model.c}
#     assert set(model.eq3.equations) == {model.x.derive() << 1 * model.c}


# @mark.parametrize("f", [non_instance, instance])
# def test_mass_action(f):
#     class Model(Compartment):
#         x: Species = initial(default=0)
#         c: Constant = assign(default=0, constant=True)
#         eq1 = MassAction(reactants=[x], products=[], rate=c)
#         eq2 = MassAction(reactants=[], products=[x], rate=c)
#         eq3 = MassAction(reactants=[2 * x], products=[3 * x], rate=c)

#     model: Model = f(Model)
#     assert model.x.equation_order == 1
#     assert set(model.eq1.equations) == {
#         model.x.derive() << -1 * (model.c * (model.x**1))
#     }
#     assert set(model.eq2.equations) == {model.x.derive() << 1 * model.c}
#     assert set(model.eq3.equations) == {
#         model.x.derive() << 1 * (model.c * (model.x**2))
#     }


# def test_duplicate_species():
#     class Duplicate(Compartment):
#         x: Species = initial(default=1)
#         eq = MassAction(reactants=[x, x], products=[], rate=1)

#     class Double(Compartment):
#         x: Species = initial(default=1)
#         eq = MassAction(reactants=[2 * x], products=[], rate=1)

#     times = np.linspace(0, 1, 10)
#     duplicate = Simulator(Duplicate).solve(save_at=times)
#     double = Simulator(Double).solve(save_at=times)
#     assert np.allclose(duplicate, double)


# def test_simulator():
#     class Model(Compartment):
#         x: Species = initial(default=1)
#         k: Parameter = assign(default=1)
#         eq = MassAction(reactants=[x], products=[], rate=k)

#     sim = Simulator(Model)
#     assert set(sim.compiled.variables) == {Model.x}
#     assert set(sim.compiled.parameters) == {Model.k}
#     assert sim.compiled.mapper == {Model.x: 1, Model.k: 1}
#     assert set(sim.transform.output) == {"x"}

#     times = np.linspace(0, 1, 10)
#     result = sim.solve(save_at=times)
#     assert np.allclose(result["x"], np.exp(-times), rtol=1e-3, atol=1e-3)

#     assert sim.create_problem({Model.x: 2}).y[0] == 2
#     assert sim.create_problem({Model.x: 2}).y[0] == 2


# def test_transform():
#     class Model(Compartment):
#         x: Species = initial(default=1)
#         k: Parameter = assign(default=1)
#         eq = MassAction(reactants=[x], products=[], rate=k)

#     times = np.linspace(0, 1, 10)

#     result = Simulator(Model).solve(save_at=times)
#     result2 = Simulator(Model, transform={"double": 2 * Model.x}).solve(save_at=times)

#     assert np.allclose(result2["double"], 2 * result["x"])
