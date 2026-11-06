# Changelog

## Unreleased

- Added `notebook_report` to show a model report with a reactions section in marimo or Jupyter notebooks. Requires the modular `notebook_report` in poincare (unreleased).
- `latex_reactions` takes `format="markdown"` to use `$$` display math.
- fix: the reactions LaTeX block no longer starts with an empty line.
- fix: SBML and MathML import work on Python < 3.14 (they failed with `NameError: name 'types' is not defined`).
- fix: MathML function definitions are imported correctly.
- `substitute_by_name` moved from `simbio.io.sbml.substitute_by_name` to `simbio.io.substitute_by_name`.

## 1.1.0

- Updated poincare dependency to 1.2.0, brings breaking changes in values, transform and simulator API (with_values/transform/simulator instead of as argument) and in switching warning on wrong simulation units to error.
- `model_report` now includes a reactions section.

## 1.1.0

- Exposed `model_report()` from poincare to generate reports with model's equations, variables and parameters in LaTeX.
- Added support for stochastic simulations with rebop in reactions.
- Update poincare dependency 1o 1.1.0.