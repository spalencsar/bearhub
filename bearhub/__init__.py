"""
Temporary namespace migration shim.

Canonical implementation still lives in the `bauh` package.
New code should import from `bearhub` whenever possible.
"""

from bauh import __app_name__, __version__, ROOT_DIR

__all__ = ["__app_name__", "__version__", "ROOT_DIR"]
