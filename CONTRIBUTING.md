# Developer Contribution Guide
Contribute to the repository by opening a pull request.

- [Developer Contribution Guide](#developer-contribution-guide)
  - [Local](#local)
    - [Merge the `main` Branch](#merge-the-main-branch)
    - [Run Tests](#run-tests)
    - [Install and Run `pre-commit`](#install-and-run-pre-commit)
  - [Continuous Integration](#continuous-integration)
    - [Testing](#testing)
    - [Building](#building)
    - [Releasing](#releasing)
      - [Changelog](#changelog)
        - [Changelog Style](#changelog-style)


## Local
Develop code locally by cloning the source code, creating a development environment and installing it.

1. Install [mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html), then launch the `Miniforge Prompt`.

2. Clone the `main` branch of `eqt` locally, and navigate into where it has been cloned:
```sh
# Clone (download) source code
git clone git@github.com:TomographicImaging/eqt.git
cd eqt
```

3. Create the mamba environment using the following command:
```sh
# Create environment
mamba env create -f recipe/eqt_env.yml
```

4. Activate the environment:
```sh
mamba activate eqt_env
```

5. Install the dependencies:
```sh
# Install test dependencies
pip install .[dev]
```

### Merge the `main` Branch
Conflicts may exist if your branch is behind the `main` branch. To resolve conflicts between branches, merge the `main` branch into your current working branch:
```sh
git merge main
```

### Run Tests
Before merging a pull request, all tests must pass. These can be run locally from the repository folder:
```sh
pytest
```

### Install and Run `pre-commit`
Adhere to our styling guide by installing [`pre-commit`](https://pre-commit.com) in your local eqt environment:
```sh
pip install pre-commit
pre-commit install
```

From your local repository folder, run `pre-commit` on all the files before committing:
```sh
pre-commit run -a
```
OR,

Run `pre-commit` on a single file by specifying its file path:
```sh
pre-commit run --files [path]
```
The [`.pre-commit-config.yaml`](./.pre-commit-config.yaml) config file indicates the repositories and the hooks which will be applied automatically.

## Continuous Integration
GitHub Actions automatically runs a subset of the unit tests on every commit via [`test.yml`](.github/workflows/test.yml).

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
Located in [`CHANGELOG.md`](./CHANGELOG.md).

##### Changelog Style
The changelog file needs to be updated manually every time a pull request (PR) is submitted:
- Itemise the message with "-".
- Be concise by explaining the overall changes in only a few words.
- Mention the relevant PR in brackets.

Example:
```md
# Version x.x.x
- Add `title` to `FormDockWidget` & update tests/examples (#102)
```
