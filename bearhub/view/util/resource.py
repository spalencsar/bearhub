import os

from bearhub import ROOT_DIR

_LEGACY_BAUH_ROOT = os.path.join(os.path.dirname(ROOT_DIR), 'bauh')


def get_path(resource_path: str) -> str:
    """
    Prefer bearhub resources, but keep backward compatibility with the
    historical bauh resource tree while migration is in progress.
    """
    new_base = os.path.join(ROOT_DIR, 'view', 'resources')
    new_path = os.path.join(new_base, resource_path)

    if any(ch in resource_path for ch in ('*', '?', '[')):
        return new_path

    if os.path.exists(new_path):
        return new_path

    legacy_base = os.path.join(_LEGACY_BAUH_ROOT, 'view', 'resources')
    return os.path.join(legacy_base, resource_path)
