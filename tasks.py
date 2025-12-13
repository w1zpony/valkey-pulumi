"""Invoke tasks for project management.

This file provides convenient commands for common development tasks.
Run `invoke --list` to see all available tasks.
"""

import os
import sys
from pathlib import Path

# import webbrowser  # Uncomment if needed for docs task

from invoke import task

# Project root directory
ROOT_DIR = Path(__file__).parent.resolve()
SRC_DIR = ROOT_DIR / "src"
TESTS_DIR = ROOT_DIR / "tests"
DOCS_DIR = ROOT_DIR / "docs"


def _run_command(cmd, **kwargs):
    """Run a command and handle errors."""
    print(f"Running: {cmd}")
    result = os.system(cmd)
    if result != 0:
        print(f"Command failed with exit code {result}")
        sys.exit(result)
    return result


@task
def install(c):
    """Install project dependencies."""
    print("Installing project dependencies...")

    # Install mise and tools if not already installed
    # This will also trigger the postinstall hook to create hatch environment
    _run_command("mise install")

    # Install pre-commit hooks
    _run_command("pre-commit install")

    print("✅ Dependencies installed successfully!")


@task
def format(c, check=False):
    """Format code using ruff.

    Args:
        check: Check formatting without making changes.
    """
    cmd = "hatch run ruff format --check ." if check else "hatch run ruff format ."
    _run_command(cmd)


@task
def lint(c, fix=False):
    """Run linting with ruff.

    Args:
        fix: Automatically fix linting issues.
    """
    cmd = "hatch run ruff check --fix ." if fix else "hatch run ruff check ."
    _run_command(cmd)


@task
def precommit(c, all_files=False):
    """Run pre-commit hooks.

    Args:
        all_files: Run on all files instead of just staged files.
    """
    cmd = "pre-commit run --all-files" if all_files else "pre-commit run"
    _run_command(cmd)


@task
def test(c, verbose=False, coverage=False):
    """Run tests using pytest.

    Args:
        verbose: Show verbose output.
        coverage: Generate coverage report.
    """
    cmd = "hatch run pytest tests/"

    if verbose:
        cmd += " -v"

    if coverage:
        cmd += " --cov=valkey_pulumi --cov-report=html --cov-report=term"

    _run_command(cmd)


@task
def docs(c, build=False, open_browser=False, clean=False):
    """Build and manage documentation.

    Args:
        build: Build the documentation.
        open_browser: Open documentation in browser.
        clean: Clean build files.
    """
    if clean:
        _run_command("hatch run docs:clean")

    if build:
        _run_command("hatch run docs:build")

    if open_browser:
        _run_command("hatch run docs:open")


@task
def clean(c, docs=False, cache=False, all=False):
    """Clean project files.

    Args:
        docs: Clean documentation build files.
        cache: Clean Python cache files.
        all: Clean all of the above.
    """
    if docs or all:
        _run_command("hatch run docs:clean")

    if cache or all:
        _run_command("find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true")
        _run_command("find . -type f -name '*.pyc' -delete")
        _run_command("find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true")
        _run_command("find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true")
        _run_command("find . -type d -name '.coverage' -exec rm -rf {} + 2>/dev/null || true")
        _run_command("find . -type f -name '.coverage' -delete")


@task
def build(c, dist=False):
    """Build the project.

    Args:
        dist: Build distribution packages.
    """
    if dist:
        _run_command("hatch build")
    else:
        _run_command("hatch env create")


@task
def serve_docs(c, port=8000):
    """Serve documentation locally for development.

    Args:
        port: Port to serve on.
    """
    # First build the docs
    _run_command("hatch run docs:build")

    # Serve the built documentation
    docs_build_dir = DOCS_DIR / "_build" / "html"
    os.chdir(docs_build_dir)
    _run_command(f"python -m http.server {port}")


@task
def check(c):
    """Run all checks: format, lint, and tests."""
    print("🔍 Running all checks...")

    # Check formatting
    print("Checking code formatting...")
    _run_command("hatch run ruff format --check .")

    # Check linting
    print("Running linting checks...")
    _run_command("hatch run ruff check .")

    # Run tests
    print("Running tests...")
    _run_command("hatch run test")

    print("✅ All checks passed!")


@task
def setup_dev(c):
    """Set up the complete development environment."""
    print("🚀 Setting up development environment...")

    # Install dependencies
    install(c)

    # Run initial checks to ensure everything is working
    check(c)

    print("✅ Development environment is ready!")


# Namespace for better organization
ns = task(
    format=format,
    lint=lint,
    precommit=precommit,
    test=test,
    docs=docs,
    clean=clean,
    build=build,
    serve_docs=serve_docs,
    check=check,
    install=install,
    setup_dev=setup_dev,
)
