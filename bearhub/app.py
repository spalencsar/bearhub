"""
Temporary namespace migration shim for application entry points.
"""

from bauh.app import main, tray

__all__ = ["main", "tray"]
