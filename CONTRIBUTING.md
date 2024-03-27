# Developer Contribution Guide
Contribute to the repository by opening a pull request.

## Local
Develop code locally by cloning the source code and installing it.

```sh
# Clone (download) source code
git clone git@github.com:TomographicImaging/eqt
cd eqt
# Install test dependencies
pip install .[dev]
```

### Run tests
Before merging a pull request, all tests must pass. These can be run locally from the repository folder
```sh
pytest
```
### Pre-commit guide
Adhere to our styling guide by installing [pre-commit](https://pre-commit.com) in your local eqt environment.
```sh
pip install pre-commit
pre-commit install
```
From your local repository folder, run pre-commit on all the files before committing
```sh
pre-commit run -a
```
or run pre-commit on a single file by specifying its file path
```sh
pre-commit run --files [path]
```
The [.pre-commit-config.yaml](./.pre-commit-config.yaml) config file indicates the repositories and the hooks which will be applied automatically.

## Continuous integration

GitHub Actions runs automatically a subset of the unit tests on every commit via [test.yml](.github/workflows/test.yml).

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

The `<body>` should be taken from the changelog (below).

#### Changelog
Located in [CHANGELOG.md](./CHANGELOG.md).

##### Changelog style
The changelog file needs to be updated manually every time a pull request (PR) is submitted.
- Itemise the message with "-".
- Be concise by explaining the overall changes in only a few words.
- Mention the relevant PR in brackets.

###### Example:
- Adds `title` to `FormDockWidget` & update tests/examples (#102)
