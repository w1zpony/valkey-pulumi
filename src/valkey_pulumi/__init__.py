from importlib.metadata import version

from . import example

__all__ = ["example"]

__version__ = version("valkey-pulumi")
