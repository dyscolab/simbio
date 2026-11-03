from collections.abc import Callable, Mapping
from functools import partial
from typing import Literal

from poincare import System
from poincare.printing.latex import Latex, ToLatex, default_sections, normalize_eq
from poincare.printing.latex import model_report as _model_report
from poincare.printing.notebook_display import Markdown, default_notebook_sections
from poincare.printing.notebook_display import notebook_report as _notebook_report
from poincare.reactions import RateLaw, Reactant
from symbolite.ops import substitute


def reaction_to_latex(reaction: RateLaw, latex: ToLatex) ->  Latex:
    lhs = " + ".join(map(lambda x: reactant_to_latex(x, latex), reaction.reactants))
    rhs = " + ".join(map(lambda x: reactant_to_latex(x, latex), reaction.products))
    rate_law = normalize_eq(reaction.rate_law, transform=latex.transform, base = latex.system)

    return f"{lhs} &\\rightarrow {rhs},\\quad \\text{{rate:}}\\ {rate_law}"

def reactant_to_latex(reactant: Reactant,latex: ToLatex) ->  Latex:
    return f"{reactant.stoichiometry if reactant.stoichiometry != 1 else ""} {substitute(reactant.variable, latex.transform)}"


def aligned_reactions(model: type[System], latex: ToLatex) -> Latex:
    lines = ["\\begin{aligned}"]
    lines.extend(
        reaction_to_latex(reaction=reaction, latex=latex) + "\\\\"
        for reaction in model._yield(RateLaw)
    )
    lines.append("\\end{aligned}")
    return "\n".join(lines)


def latex_reactions(
    model: type[System],
    transform: dict | None = None,
    latex: ToLatex | None = None,
    format: Literal["latex", "markdown"] = "latex",
) -> Latex:
    if latex is None:
        transform = transform if transform is not None else {}
        latex = ToLatex(model, transform=transform)
    aligned = aligned_reactions(model=model, latex=latex)
    if format == "latex":
        return "\\[ " + aligned + " \\]"
    # Markdown renderers escape \[ \], so use $$ display math instead.
    return "$$\n" + aligned + "\n$$"


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


def notebook_report(
    model: type[System],
    transform: dict | None = None,
    descriptions: dict | None = None,
    replace_algebraics: bool = False,
    sections: Mapping[str, Callable[[type[System], ToLatex], Markdown]] = {
        "Reactions": partial(latex_reactions, format="markdown")
    }
    | default_notebook_sections,
    level: int = 2,
    show: bool = True,
) -> Markdown | None:
    return _notebook_report(
        model=model,
        transform=transform,
        descriptions=descriptions,
        replace_algebraics=replace_algebraics,
        sections=sections,
        level=level,
        show=show,
    )
