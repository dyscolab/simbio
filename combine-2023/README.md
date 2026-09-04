# simbio tutorial @ COMBINE 2023

This directory contains the simbio's slides and tutorial
used at [COMBINE 2023](https://co.mbine.org/author/combine-2023/).

- [slides](slides/slides.html)
- [tutorial](tutorial.ipynb)

## Running the tutorial

The simplest option is to open the notebook in Google Colab
with the following link:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hgrecco/simbio/blob/combine-2023/combine-2023/tutorial.ipynb)

The recommended option is to use VS Code or some other IDE.

simbio can be installed via `pip` or `uv`:

```sh
uv pip install simbio[io]
```

We also provide a `pixi.toml` to create a conda enviroment:

```sh
pixi install
```

## Render the slides

```sh
pixi run render
```