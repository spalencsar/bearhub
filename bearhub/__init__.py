import os

__version__ = '0.10.7'
__app_name__ = 'bearhub'

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = ["__app_name__", "__version__", "ROOT_DIR"]