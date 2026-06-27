import importlib
import inspect
import os
from logging import Logger
from typing import Dict, Generator, List, Optional, Tuple

from bearhub import ROOT_DIR as BEARHUB_ROOT_DIR, __app_name__
from bearhub.api.abstract.controller import ApplicationContext, SoftwareManager
from bearhub.view.util import translation

_LEGACY_BAUH_ROOT = os.path.join(os.path.dirname(BEARHUB_ROOT_DIR), 'bauh')

FORBIDDEN_GEMS_FILE = f'/etc/{__app_name__}/gems.forbidden'


def find_manager(member):
    if not isinstance(member, str):
        if inspect.isclass(member) and inspect.getmro(member)[1].__name__ == 'SoftwareManager':
            return member
        elif inspect.ismodule(member):
            for name, mod in inspect.getmembers(member):
                manager_found = find_manager(mod)
                if manager_found:
                    return manager_found


def read_forbidden_gems() -> Generator[str, None, None]:
    try:
        with open(FORBIDDEN_GEMS_FILE) as f:
            forbidden_lines = f.readlines()

        for line in forbidden_lines:
            clean_line = line.strip()

            if clean_line and not clean_line.startswith('#'):
                yield clean_line

    except FileNotFoundError:
        pass


def _discover_gem_dirs() -> List[Tuple[str, str]]:
    gems: Dict[str, str] = {}

    for root in (BEARHUB_ROOT_DIR, _LEGACY_BAUH_ROOT):
        gems_dir = os.path.join(root, 'gems')
        if not os.path.isdir(gems_dir):
            continue

        for entry in os.scandir(gems_dir):
            if entry.is_dir() and entry.name != '__pycache__' and entry.name not in gems:
                gems[entry.name] = entry.path

    return sorted(gems.items())


def _import_controller_module(gem_name: str):
    for module_name in (f'bearhub.gems.{gem_name}.controller', f'bauh.gems.{gem_name}.controller'):
        try:
            return importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue

    return None


def load_managers(locale: str, context: ApplicationContext, config: dict, default_locale: str, logger: Logger) -> List[SoftwareManager]:
    managers = []

    forbidden_gems = {gem for gem in read_forbidden_gems()}

    for gem_name, gem_path in _discover_gem_dirs():
        if gem_name in forbidden_gems:
            logger.warning(f"gem '{gem_name}' could not be loaded because it was marked as forbidden in '{FORBIDDEN_GEMS_FILE}'")
            continue

        module = _import_controller_module(gem_name)

        if module:
            manager_class = find_manager(module)

            if manager_class:
                if locale:
                    locale_path = f'{gem_path}/resources/locale'

                    if os.path.exists(locale_path):
                        context.i18n.current.update(translation.get_locale_keys(locale, locale_path)[1])

                        if default_locale and context.i18n.default:
                            context.i18n.default.update(translation.get_locale_keys(default_locale, locale_path)[1])

                man = manager_class(context=context)

                if config['gems'] is None:
                    man.set_enabled(man.is_default_enabled())
                else:
                    man.set_enabled(gem_name in config['gems'])

                managers.append(man)

    return managers