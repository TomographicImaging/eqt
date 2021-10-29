# GitHub Actions

## Building the Conda Package: [conda_build_and_publish.yml](https://github.com/paskino/qt-elements/blob/main/.github/workflows/conda_build_and_publish.yml)
This github action builds and tests the conda package, by using the [conda-package-publish-action](https://github.com/paskino/conda-package-publish-action)

When pushing to main *all* variants are built and tested.

When making an [annotated](https://git-scm.com/book/en/v2/Git-Basics-Tagging) tag, *all* variants are built, tested and published to the [paskino conda channel for qt-elements](https://anaconda.org/paskino/eqt/files). This package is noarch.

When opening or modifying a pull request to main, a single variant is built and tested, but not published. This variant is `python=3.7` and `numpy=1.18`.

## Building the PyPi Package: [pypi_publish.yml](https://github.com/paskino/qt-elements/blob/main/.github/workflows/pypi_publish.yml)
This github action builds the pypi package, by using the [deploy-pypi action](https://github.com/casperdcl/deploy-pypi).

When pushing to main it is built and checked.

When making an [annotated](https://git-scm.com/book/en/v2/Git-Basics-Tagging) tag, it is built and published to the [PyPi](https://pypi.org/project/eqt/#description).
