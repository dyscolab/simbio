from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Any,
)

from poincare import (
    Derivative,
    Variable,
)
from poincare._node import Node, NodeMapper
from poincare.reactions import (
    Reactant,
)
from poincare.reactions.reactions import (
    compensate_volume,
    make_concentration,
)
from poincare.types import (
    Initial,
    System,
)
from symbolite import Real, substitute

if TYPE_CHECKING:
    pass


def is_instance_or_subclass(obj: Any, cls: type):
    try:
        return issubclass(obj, cls) or isinstance(obj, cls)
    except TypeError:
        return isinstance(obj, cls)


def first_system_parent(obj: Node | None) -> System | type[System] | None:
    if isinstance(obj, Node):
        parent = getattr(obj, "parent", None)
        if is_instance_or_subclass(parent, System):
            return parent
        else:
            return first_system_parent(parent)
    else:
        return None


def concentration(*, default: Initial | None = None):
    return Species(initial=default, concentration=True)


def amount(*, default: Initial | None = None):
    return Species(initial=default, concentration=False)


def reaction_concentration(*, default: Initial | None = None):
    return Reactant(
        variable=Species(initial=default, concentration=True), stoichiometry=1
    )


def reaction_amount(*, default: Initial | None = None):
    return Reactant(
        variable=Species(initial=default, concentration=False), stoichiometry=1
    )


def volume(*, default: Initial | None = None):
    return Volume(initial=default)


class Species(Variable):
    def __init__(self, *, initial: Initial, concentration: bool):
        self.concentration = concentration
        super().__init__(initial=initial)

    def _copy_from(self, parent: Node):
        mapper = NodeMapper(parent)
        copy = self.__class__(
            initial=substitute(self.initial, mapper), concentration=self.concentration
        )
        for order, der in self.derivatives.items():
            copy.derivatives[order] = Derivative(
                copy, initial=substitute(der.initial, mapper), order=order
            )
        copy.equation_order = self.equation_order
        return copy


@compensate_volume.register
def compensate_volume_Species(
    species: Species, rhs: Real | Initial, reaction_is_concentration: bool
) -> Real | Initial:
    system_parent = first_system_parent(species)
    if is_instance_or_subclass(system_parent, Compartment):
        if species.concentration and not reaction_is_concentration:
            return rhs / system_parent._volume
        elif not species.concentration and reaction_is_concentration:
            return rhs * system_parent._volume
        else:
            return rhs
    else:
        return rhs


@make_concentration.register
def make_concentration_Species(species: Species) -> Real | Initial:
    system_parent = first_system_parent(species)
    if not species.concentration and (
        is_instance_or_subclass(system_parent, Compartment)
    ):
        try:
            return species / system_parent._volume
        except AttributeError as err:
            if not hasattr(system_parent, "_volume"):
                raise AttributeError("Compartments must have a Volume")
            else:
                raise err
    else:
        return species


# def verify_species_units(initial):
#     if isinstance(initial, pint.Quantity):
#         if (
#             initial.dimensionality == concetration_dim
#             or initial.dimensionality == substance_dim
#         ):
#             return
#         else:
#             raise TypeError(
#                 f"Species must have concentration or substance dimensionality"
#             )
#     else:
#         raise TypeError(
#             f"Species does not have units, must have units of substance or concentration"
#         )


class Volume(Variable):
    def __set_name__(self, cls: Node, name: str):
        super().__set_name__(cls, name)
        if cls is not None:
            setattr(cls, "_volume", self)


class Compartment(System, abstract=True):
    def __init_subclass__(cls, **kwargs) -> None:
        volumes = set(cls._yield(Volume, recursive=False))
        if len(volumes) == 0:
            raise AttributeError("Compartments must have a Volume")
        elif len(volumes) > 1:
            raise AttributeError("Compartments can only have one Volume")
        super().__init_subclass__(**kwargs)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if isinstance(getattr(self.__class__, key, None), Species | Volume):
                if isinstance(value, Node):
                    raise TypeError(
                        "Compartment Species and Volume cannot be linked to external variables, only initials can be passed on instantiation"
                    )
        super().__init__(*args, **kwargs)
