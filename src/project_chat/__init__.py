from __future__ import annotations

from importlib import import_module
from pathlib import Path


def import_python(root: Path):
    """
    Imports Python modules from a specified directory and its subdirectories,
    yielding their names.
    :param root: The root directory from which to import Python modules.
    :return: Yields module names as strings.
    """
    for module_path in root.glob("*.py"):
        if module_path.name in ("__init__.py", "pycache", "__pycache__"):
            continue
        if module_path.is_file():
            relative_path = module_path.relative_to(Path(__file__).parent)
            subfolders = "".join(map(".{}".format, relative_path.parts[:-1]))
            str_path = module_path.with_suffix("").name
            import_module("." + str_path, __name__ + subfolders)
            yield module_path.with_suffix("").name
            continue
        yield from import_python(module_path)


__all__ = list(import_python(Path(__file__).parent))
