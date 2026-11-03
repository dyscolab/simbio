from . import MassAction, System, Variable, initial, model_report, notebook_report


class Model(System):
    A: Variable = initial(default=1)
    B: Variable = initial(default=0)
    conversion = MassAction(reactants=[A], products=[2 * B], rate=1)


def test_model_report_reactions():
    output = model_report(Model)
    assert "\\subsection{Reactions}" in output
    assert "\\rightarrow" in output


def test_notebook_report_reactions():
    output = notebook_report(Model, show=False)
    assert output.startswith("## Reactions\n\n$$")
    assert "\\rightarrow" in output
    assert "\\[" not in output
