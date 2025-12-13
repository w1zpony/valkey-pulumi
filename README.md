# valkey-pulumi

[![Tests][badge-tests]][tests]
[![Documentation][badge-docs]][documentation]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/daotl/valkey-pulumi/test.yaml?branch=main
[badge-docs]: https://img.shields.io/readthedocs/valkey-pulumi

Valkey Pulumi + Docker deployment

## Getting started

Please refer to the [documentation][],
in particular, the [API documentation][].

### Quick Start with Invoke Tasks

This project includes [invoke](https://www.pyinvoke.org/) tasks to simplify development workflows:

```bash
# First-time setup: install tools and create environment
mise install

**Note**: After running `mise install`, the postinstall hook automatically creates the hatch environment and installs project dependencies (including invoke), making invoke available for use.

# Install all dependencies and set up the development environment
invoke setup-dev

# Run all checks (formatting, linting, and tests)
invoke check

# Format code
invoke format

# Run linting with auto-fix
invoke lint --fix

# Run tests
invoke test

# Build and serve documentation locally
invoke docs --build --open-browser

# Clean all generated files
invoke clean --all

# See all available tasks
invoke --list
```

## Installation

You need to have Python 3.11 or newer installed on your system.
We recommend using [mise][] to manage Python versions and tools.

There are several alternative options to install valkey-pulumi:

<!--
1) Install the latest release of `valkey-pulumi` from [PyPI][]:

```bash
pip install valkey-pulumi
```
-->

1. Install the latest development version:

```bash
pip install git+https://github.com/daotl/valkey-pulumi.git@main
```

## Release notes

See the [changelog][].

## Contact

For questions and help requests, you can reach out in the [scverse discourse][].
If you found a bug, please use the [issue tracker][].

## Citation

> t.b.a

[uv]: https://github.com/astral-sh/uv
[mise]: https://mise.dev/
[scverse discourse]: https://discourse.scverse.org/
[issue tracker]: https://github.com/daotl/valkey-pulumi/issues
[tests]: https://github.com/daotl/valkey-pulumi/actions/workflows/test.yaml
[documentation]: https://valkey-pulumi.readthedocs.io
[changelog]: https://valkey-pulumi.readthedocs.io/en/latest/changelog.html
[api documentation]: https://valkey-pulumi.readthedocs.io/en/latest/api.html
[pypi]: https://pypi.org/project/valkey-pulumi
