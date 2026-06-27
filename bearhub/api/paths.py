import os
import shutil
from getpass import getuser
from pathlib import Path

from bauh import __app_name__
from bauh.api import user


def get_temp_dir(username: str) -> str:
    return f'/tmp/{__app_name__}@{username}'


CACHE_DIR = f'/var/cache/{__app_name__}' if user.is_root() else f'{Path.home()}/.cache/{__app_name__}'
CONFIG_DIR = f'/etc/{__app_name__}' if user.is_root() else f'{Path.home()}/.config/{__app_name__}'
USER_THEMES_DIR = f'/usr/share/{__app_name__}/themes' if user.is_root() else f'{Path.home()}/.local/share/{__app_name__}/themes'
DESKTOP_ENTRIES_DIR = '/usr/share/applications' if user.is_root() else f'{Path.home()}/.local/share/applications'
TEMP_DIR = get_temp_dir(getuser())
LOGS_DIR = f'{TEMP_DIR}/logs'
AUTOSTART_DIR = f'/etc/xdg/autostart' if user.is_root() else f'{Path.home()}/.config/autostart'
BINARIES_DIR = f'/usr/local/bin' if user.is_root() else f'{Path.home()}/.local/bin'
SHARED_FILES_DIR = f'/usr/local/share/{__app_name__}' if user.is_root() else f'{Path.home()}/.local/share/{__app_name__}'


def _migrate_dir_if_possible(old_path: str, new_path: str):
    if old_path == new_path:
        return

    if not os.path.exists(old_path):
        return

    if os.path.exists(new_path):
        return

    try:
        parent = os.path.dirname(new_path)
        if parent:
            Path(parent).mkdir(parents=True, exist_ok=True)

        shutil.move(old_path, new_path)
    except Exception:
        # The migration is best-effort. If it fails, the app can still start with empty defaults.
        pass


def migrate_legacy_paths():
    old_app_name = 'bauh'

    if old_app_name == __app_name__:
        return

    if user.is_root():
        old_cache = f'/var/cache/{old_app_name}'
        old_config = f'/etc/{old_app_name}'
        old_shared = f'/usr/local/share/{old_app_name}'
        old_temp = f'/tmp/{old_app_name}@{getuser()}'
    else:
        home = Path.home()
        old_cache = f'{home}/.cache/{old_app_name}'
        old_config = f'{home}/.config/{old_app_name}'
        old_shared = f'{home}/.local/share/{old_app_name}'
        old_temp = f'/tmp/{old_app_name}@{getuser()}'

    _migrate_dir_if_possible(old_cache, CACHE_DIR)
    _migrate_dir_if_possible(old_config, CONFIG_DIR)
    _migrate_dir_if_possible(old_shared, SHARED_FILES_DIR)
    _migrate_dir_if_possible(old_temp, TEMP_DIR)


migrate_legacy_paths()
