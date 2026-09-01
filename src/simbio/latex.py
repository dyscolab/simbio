from collections.abc import Iterable, Callable, Mapping

from poincare.reactions import RateLaw, Reactant
from poincare.printing.latex import Latex, ToLatex, normalize_eq, default_sections
from poincare.printing.latex import model_report as _model_report
from symbolite.ops import translate, substitute
from symbolite.impl import liblatex
from poincare import System



def reaction_to_latex(reaction: RateLaw, latex: ToLatex) ->  Latex:
    lhs = " + ".join(map(lambda x: reactant_to_latex(x, latex), reaction.reactants))
    rhs = " + ".join(map(lambda x: reactant_to_latex(x, latex), reaction.products))
    rate_law = normalize_eq(reaction.rate_law, transform=latex.transform, base = latex.system)

    return f"{lhs} &\\rightarrow {rhs},\\quad \\text{{rate:}}\\ {rate_law}"

def reactant_to_latex(reactant: Reactant,latex: ToLatex) ->  Latex:
    return f"{reactant.stoichiometry if reactant.stoichiometry != 1 else ""} {substitute(reactant.variable, latex.transform)}"


def yield_reactions(model: type[System], latex: ToLatex) -> Iterable[Latex]:
    for reaction in model._yield(RateLaw):
        yield reaction_to_latex(reaction=reaction, latex= latex)


def aligned_reactions(iterable)-> Latex:
    lines = []
    lines.append("\\begin{aligned}")
    lines.extend(iterable)
    lines.append("\\end{aligned}")
    return "\\\\\n".join(lines)


def latex_reactions(
    model: type[System], transform: dict | None = None, latex: ToLatex | None = None
) -> Latex:
    if latex is None:
        transform = transform if transform is not None else {}
        latex = ToLatex(model, transform=transform)
    return "\\[ " + aligned_reactions(yield_reactions(model = model, latex=latex)) + " \\]"


def model_report(
    model: type[System],
    path: str | None = None,
    transform: dict | None = None,
    descriptions: dict | None = None,
    standalone: bool = True,
    replace_algebraics: bool = False,
    sections: Mapping[
        str, Callable[[type[System], ToLatex], str]
    ] = {"Reactions": latex_reactions} | default_sections 
) -> Latex | None:
    return _model_report(
        model=model,
        path=path,
        transform=transform,
        descriptions=descriptions,
        standalone=standalone,
        replace_algebraics=replace_algebraics,
        sections=sections,
    )




    

