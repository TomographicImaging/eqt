# GitHub Actions

Runs automatically on every commit via [test.yml](./test.yml).

## Testing

Runs `pytest`.

## Building

Runs automatically after tests (above) succeed.

Builds binary (`*.whl`) & source (`*.tar.gz`) distributions.

## Releasing

Runs automatically -- when a [tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging) is pushed -- after builds (above) succeed.

Publishes to [PyPI](https://pypi.org/project/eqt) and drafts changelog (release notes) at <https://github.com/paskino/qt-elements/releases>.

:warning: The draft notes above need to be manually tidied & approved by a maintainer.
