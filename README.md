# simbio

[![Copier Badge][copier-badge]][copier-url]
[![Pixi Badge][pixi-badge]][pixi-url]
![License][license-badge]
[![CI Badge][ci-badge]][ci-url]
[![conda-forge Badge][conda-forge-badge]][conda-forge-url]
[![PyPI Badge][pypi-badge]][pypi-url]
[![Python version Badge][pypi-version-badge]][pypi-version-url]

A Python-based package for simulation of Chemical Reaction Networks (CRNs).
It extends [`poincare`](https://github.com/maurosilber/poincare),
a package for modelling dynamical systems,
to add functionality for CRNs.

## Usage

To create a system with two species $A$ and $B$
and a reaction converting $2A \\rightarrow B$ with rate 1:

```python
>>> from simbio import Compartment, Species, RateLaw, initial
>>> class Model(Compartment):
...    A: Species = initial(default=1)
...    B: Species = initial(default=0)
...    r = RateLaw(
...        reactants=[2 * A],
...        products=[B],
...        rate_law=1,
...    )
```

This corresponds to the following system of equations

$$
\\begin{cases}
\\frac{dA}{dt} = -2 \\
\\frac{dB}{dt} = +1
\\end{cases}
$$

with initial conditions

$$
\\begin{cases}
A(0) = 1 \\
B(0) = 0
\\end{cases}
$$

In CRNs,
we usually deal with [mass-action](https://en.wikipedia.org/wiki/Law_of_mass_action) reactions.
Using `MassAction` instead of `Reaction` automatically adds the reactants to the rate law:

```python
>>> from simbio import MassAction
>>> class MassActionModel(Compartment):
...    A: Species = initial(default=1)
...    B: Species = initial(default=0)
...    r = MassAction(
...        reactants=[2 * A],
...        products=[B],
...        rate=1,
...    )
```

generating the following equations:

$$
\\begin{cases}
\\frac{dA}{dt} = -2 A^2 \\
\\frac{dB}{dt} = +1 A^2
\\end{cases}
$$

To simulate the system,
use the `Simulator.solve` which outputs a `pandas.DataFrame`:

```python
>>> from simbio import Simulator
>>> Simulator(MassActionModel).solve(save_at=range(5))
             A         B
time
0     1.000000  0.000000
1     0.333266  0.333367
2     0.199937  0.400032
3     0.142798  0.428601
4     0.111061  0.444470
```

For more details into SimBio's capabilities,
we recommend reading [poincaré's README](https://github.com/maurosilber/poincare).

## SBML

SimBio can import models from Systems Biology Markup Language (SBML) files:

```python
>>> from simbio.io import sbml
>>> sbml.load("repressilator.sbml")
Elowitz2000 - Repressilator
-----------------------------------------------------------------------------------
type          total  names
----------  -------  --------------------------------------------------------------
variables         6  PX, PY, PZ, X, Y, Z
parameters       17  cell, beta, alpha0, alpha, eff, n, KM, tau_mRNA, tau_prot, ...
equations        12  Reaction1, Reaction2, Reaction3, Reaction4, Reaction5, ...
```

or download them from the [BioModels](https://www.ebi.ac.uk/biomodels/) repository:

```python
>>> from simbio.io import biomodels
>>> biomodels.load("BIOMD12")
Elowitz2000 - Repressilator
-----------------------------------------------------------------------------------
type          total  names
----------  -------  --------------------------------------------------------------
variables         6  PX, PY, PZ, X, Y, Z
parameters       17  cell, beta, alpha0, alpha, eff, n, KM, tau_mRNA, tau_prot, ...
equations        12  Reaction1, Reaction2, Reaction3, Reaction4, Reaction5, ...
```

## Install

Using [pixi][pixi-url],
install from PyPI with:

```sh
pixi add --pypi simbio
```

or install the latest development version from GitHub with:

```sh
pixi add --pypi simbio@https://github.com/maurosilber/simbio.git
```

Otherwise,
use `pip` or your `pip`-compatible package manager:

```sh
pip install simbio  # from PyPI
pip install git+https://github.com/maurosilber/simbio.git  # from GitHub
```

## Development

This project is managed by [pixi][pixi-url].
You can install it for development using:

```sh
git clone https://github.com/maurosilber/simbio
cd simbio
pixi run pre-commit-install
```

Pre-commit hooks are used to lint and format the project.

### Testing

Run tests using:

```sh
pixi run test
```

### Publishing to PyPI

When a tagged commit is pushed to GitHub,
the GitHub Action defined in `.github/workflows/ci.yml`
builds and publishes the package to PyPI.

Tag a commit and push the tags with:

```sh
git tag <my-tag>
git push --tags
```

Trusted publishing must be enabled once in [PyPI Publishing](https://pypi.org/manage/account/publishing/).
Fill the following values in the form:

```
PyPI Project Name: simbio
            Owner: maurosilber
  Repository name: simbio
    Workflow name: ci.yml
 Environment name: pypi
```

[ci-badge]: https://img.shields.io/github/actions/workflow/status/maurosilber/simbio/ci.yml
[ci-url]: https://github.com/maurosilber/simbio/actions/workflows/ci.yml
[conda-forge-badge]: https://img.shields.io/conda/vn/conda-forge/simbio?logoColor=white&logo=conda-forge
[conda-forge-url]: https://prefix.dev/channels/conda-forge/packages/simbio
[copier-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-black.json
[copier-url]: https://github.com/copier-org/copier
[license-badge]: https://img.shields.io/badge/license-MIT-blue
[pixi-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json
[pixi-url]: https://pixi.sh
[pypi-badge]: https://img.shields.io/pypi/v/simbio.svg?logo=pypi&logoColor=white
[pypi-url]: https://pypi.org/project/simbio
[pypi-version-badge]: https://img.shields.io/pypi/pyversions/simbio?logoColor=white&logo=python
[pypi-version-url]: https://pypi.org/project/simbio
