# simbio

[![Copier Badge][copier-badge]][copier-url]
[![Pixi Badge][pixi-badge]][pixi-url]
![License][license-badge]
[![CI Badge][ci-badge]][ci-url]
[![conda-forge Badge][conda-forge-badge]][conda-forge-url]
[![PyPI Badge][pypi-badge]][pypi-url]
[![Python version Badge][pypi-version-badge]][pypi-version-url]

A Python-based package for simulation of Chemical Reaction Networks (CRNs).
It extends [`poincare`](https://github.com/dyscolab/poincare),
a package for modelling dynamical systems,
to add functionality for CRNs.

## Usage

See [simbio's documentation](https://dyscolab.github.io/simbio/) on the dyscolab page, or go directly to the [intro tutorial](https://marimo.app/github.com/dyscolab/dyscolab-tutorials/blob/main/simbio/getting_started_with_simbio.py).

## Install

Using [pixi][pixi-url],
install from PyPI with:

```sh
pixi add --pypi simbio
```

or install the latest development version from GitHub with:

```sh
pixi add --pypi simbio@https://github.com/dyscolab/simbio.git
```

Otherwise,
use `pip` or your `pip`-compatible package manager:

```sh
pip install simbio  # from PyPI
pip install git+https://github.com/dyscolab/simbio.git  # from GitHub
```

## Development

This project is managed by [pixi][pixi-url].
You can install it for development using:

```sh
git clone https://github.com/dyscolab/simbio
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

[ci-badge]: https://img.shields.io/github/actions/workflow/status/dyscolab/simbio/ci.yml
[ci-url]: https://github.com/dyscolab/simbio/actions/workflows/ci.yml
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
