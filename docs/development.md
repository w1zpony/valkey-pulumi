# Development Guide

This guide covers how to set up a development environment and work with the codebase.

## Setting Up the Development Environment

The easiest way to set up the development environment is to use the invoke tasks:

```bash
# Install all dependencies and set up the development environment
invoke setup-dev
```

This will:
- Install the required Python version using mise
- Install uv and hatch package managers
- Automatically create the hatch environment and install dependencies from pyproject.toml (via mise postinstall hook)
  - This includes installing invoke as a project dependency
- Install pre-commit hooks
- Run initial checks to ensure everything is working

## Development Workflow

### Code Quality

This project uses several tools to maintain code quality:

- **Ruff**: For Python linting and formatting
- **Biome**: For JSON/JavaScript formatting
- **Pre-commit hooks**: To run checks before commits

#### Using Invoke Tasks

```bash
# Format code
invoke format

# Check formatting without making changes
invoke format --check

# Run linting
invoke lint

# Run linting with auto-fix
invoke lint --fix

# Run all pre-commit hooks
invoke precommit

# Run pre-commit hooks on all files
invoke precommit --all-files
```

#### Manual Commands

```bash
# Format code with ruff
ruff format .

# Check and fix linting issues
ruff check --fix .

# Run all pre-commit hooks manually
pre-commit run --all-files
```

### Testing

#### Using Invoke Tasks

```bash
# Run tests
invoke test

# Run tests with verbose output
invoke test --verbose

# Run tests with coverage report
invoke test --coverage
```

#### Manual Commands

```bash
# Run tests with the current Python version
hatch run test

# Run tests with matrix configurations (3.11 and 3.14)
hatch test
```

### Documentation

#### Using Invoke Tasks

```bash
# Build documentation
invoke docs --build

# Build and open documentation in browser
invoke docs --build --open-browser

# Clean documentation build files
invoke docs --clean

# Serve documentation locally for development
invoke serve-docs --port 8000
```

#### Manual Commands

```bash
# Build documentation
hatch run docs:build

# Open documentation in browser
hatch run docs:open

# Clean documentation build files
hatch run docs:clean
```

### Building the Project

#### Using Invoke Tasks

```bash
# Build the project
invoke build

# Build distribution packages
invoke build --dist
```

#### Manual Commands

```bash
# Create hatch environment
hatch env create

# Build distribution packages
hatch build
```

### Cleaning

#### Using Invoke Tasks

```bash
# Clean documentation build files
invoke clean --docs

# Clean Python cache files
invoke clean --cache

# Clean all of the above
invoke clean --all
```

## Running All Checks

To run all checks (formatting, linting, and tests) at once:

```bash
invoke check
```

## Project Structure

```
valkey-pulumi/
├── src/valkey_pulumi/     # Source code
├── tests/                                  # Test files
├── docs/                                   # Documentation source
├── tasks.py                                # Invoke tasks
├── pyproject.toml                          # Project configuration
├── mise.toml                               # Python version specification
└── .pre-commit-config.yaml                 # Pre-commit hooks configuration
```

## Configuration

### Python Version

The project uses mise for Python version management. The required Python version and tools are specified in `mise.toml`.

### Dependencies

Dependencies are managed through hatch environments defined in `pyproject.toml`:
- `dev`: Development dependencies
- `test`: Testing dependencies
- `doc`: Documentation dependencies

### Tools

The following tools are managed by mise:
- Python 3.14
- uv for fast package installation
- hatch for environment management and project tasks

The mise configuration includes a postinstall hook that automatically runs `hatch env create` after tools are installed, which:
- Creates the hatch environment
- Installs all project dependencies from pyproject.toml (including invoke)
- Makes invoke available for task automation

### Code Style

- Line length: 120 characters
- Import sorting with isort
- Docstring formatting with pydocstyle
- Ruff for linting and formatting

### Testing

- pytest for test framework
- Coverage for test coverage reporting
- Tests run on Python 3.11 and 3.14

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run `invoke check` to ensure everything passes
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Python version not found**: Make sure mise is installed and run `mise install`
2. **uv or hatch not found**: Run `mise install` to install all specified tools
3. **invoke not found**: Run `mise install` to trigger the postinstall hook, or manually run `hatch env create`
4. **Hatch environment not created**: Run `mise install` (triggers postinstall hook) or manually run `hatch env create`
5. **Pre-commit hooks not installed**: Run `pre-commit install` or `invoke setup-dev`
6. **Tests failing**: Make sure all dependencies are installed with `invoke setup-dev`

### Getting Help

- Run `invoke --list` to see all available tasks
- Run `invoke <task> --help` to see help for a specific task
- Check the [documentation][] for more detailed information