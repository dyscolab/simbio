from __future__ import annotations
from poincare.types import EquationGroup
from symbolite import Real
from ..core import (
    Compartment,
    MassAction,
    Parameter,
    Species,
    ReactionSpecies,
    assign,
    initial,
)


class Creation(EquationGroup):
    """A substance is created from nothing at a constant rate.

    ∅ -> A
    """

    def __init__(self, A: Species | ReactionSpecies | Real, rate: float | Real):
        self.equations = MassAction(reactants=[], products=[A], rate=rate).equations


class AutoCreation(EquationGroup):
    """A substance is created at a rate proportional to its abundance.

    A -> 2A
    """

    def __init__(self, A: Species | ReactionSpecies | Real, rate: float | Real):
        self.equations = MassAction(reactants=[A], products=[A, A], rate=rate).equations


class Destruction(EquationGroup):
    """A substance degrades into nothing.

    A -> ∅
    """

    def __init__(self, A: Species | ReactionSpecies | Real, rate: float | Real):
        self.equations = MassAction(reactants=[A], products=[], rate=rate).equations


class Conversion(EquationGroup):
    """A substance convert to another.

    A -> B
    """

    def __init__(
        self,
        A: Species | ReactionSpecies | Real,
        B: Species | ReactionSpecies | Real,
        rate: float | Real,
    ):
        self.equations = MassAction(reactants=[A], products=[B], rate=rate).equations


class Synthesis(EquationGroup):
    """Two or more simple substances combine to form a more complex substance.

    A + B -> AB
    """

    def __init__(
        self,
        A: Species | ReactionSpecies | Real,
        B: Species | ReactionSpecies | Real,
        AB: Species | ReactionSpecies | Real,
        rate: float | Real,
    ):
        self.equations = MassAction(
            reactants=[A, B], products=[AB], rate=rate
        ).equations


class Dissociation(EquationGroup):
    """A more complex substance breaks down into its more simple parts.

    AB -> A + B
    """

    def __init__(
        self,
        AB: Species | ReactionSpecies | Real,
        A: Species | ReactionSpecies | Real,
        B: Species | ReactionSpecies | Real,
        rate: float | Real,
    ):
        self.equations = MassAction(
            reactants=[AB], products=[A, B], rate=rate
        ).equations
