"""
Temporary namespace migration shim for application entry points.
"""

from bearhub.app_main import main, tray

__all__ = ["main", "tray"]
