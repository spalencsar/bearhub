"""
Legacy namespace compatibility shim.

Deprecated: import from `bearhub` instead of `bauh`.
"""
from bearhub import ROOT_DIR, __app_name__, __version__

__all__ = ["__app_name__", "__version__", "ROOT_DIR"]