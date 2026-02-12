from __future__ import annotations

from .. import (
    MassAction,
    Parameter,
    Reactant,
    System,
    assign,
    reaction_initial,
)


class Creation(System):
    """A substance is created from nothing at a constant rate.

    ∅ -> A
    """

    A: Reactant = reaction_initial()
    rate: Parameter = assign()
    reaction = MassAction(reactants=[], products=[A], rate=rate)


class AutoCreation(System):
    """A substance is created at a rate proportional to its abundance.

    A -> 2A
    """

    A: Reactant = reaction_initial()
    rate: Parameter = assign()
    reaction = MassAction(reactants=[A], products=[2 * A], rate=rate)


class Destruction(System):
    """A substance degrades into nothing.

    A -> ∅
    """

    A: Reactant = reaction_initial()
    rate: Parameter = assign()
    reaction = MassAction(reactants=[A], products=[], rate=rate)


class Conversion(System):
    """A substance convert to another.

    A -> B
    """

    A: Reactant = reaction_initial()
    B: Reactant = reaction_initial()
    rate: Parameter = assign()
    reaction = MassAction(reactants=[A], products=[B], rate=rate)


class Synthesis(System):
    """Two or more simple substances combine to form a more complex substance.

    A + B -> AB
    """

    A: Reactant = reaction_initial()
    B: Reactant = reaction_initial()
    AB: Reactant = reaction_initial()
    rate: Parameter = assign()
    reaction = MassAction(reactants=[A, B], products=[AB], rate=rate)


class Dissociation(System):
    """A more complex substance breaks down into its more simple parts.

    AB -> A + B
    """

    AB: Reactant = reaction_initial()
    A: Reactant = reaction_initial()
    B: Reactant = reaction_initial()
    rate: Parameter = assign()
    reaction = MassAction(reactants=[AB], products=[A, B], rate=rate)
