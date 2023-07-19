# Developer Contribution Guide

## Local

```sh
# Clone (download) source code
git clone git@github.com:TomographicImaging/eqt
cd eqt
# Install git hooks for automatic sanity checking when trying to commit
pip install pre-commit
pre-commit install
# Install test dependencies
pip install .[dev]
# Run tests
pytest
```

## CI

GitHub Actions runs automatically on every commit via [test.yml](.github/workflows/test.yml).

### Testing

Runs `pytest`.

### Building

Runs automatically after tests (above) succeed.

Builds binary (`*.whl`) & source (`*.tar.gz`) distributions.

### Releasing

Runs automatically -- when an annotated tag is pushed -- after builds (above) succeed.

Publishes to [PyPI](https://pypi.org/project/eqt).

:warning: The annotated tag's `title` must be `Version <number without v-prefix>` (separated by a blank line) and the `body` must contain release notes, e.g.:

```sh
git tag v1.33.7 -a
```

```md
Version 1.33.7

<body>
```

The `<body>` will be used in the changelog (below).

#### Changelog

See <https://github.com/TomographicImaging/eqt/releases>, or offline:

```sh
git config --global alias.changelog 'for-each-ref --sort=-*authordate --format="# %(contents:subject)%0a%(contents:body)" refs/tags'
git changelog
```
