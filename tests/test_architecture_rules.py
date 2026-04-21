from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
MODULES_DIR = SRC_DIR / "modules"
SHARED_DIR = SRC_DIR / "shared"
SHARED_FILE_THRESHOLD = 20


def _iter_python_files(base_dir: Path) -> list[Path]:
    return sorted(path for path in base_dir.rglob("*.py") if path.is_file())


def _module_name_from_path(py_file: Path) -> str | None:
    try:
        parts = py_file.relative_to(MODULES_DIR).parts
    except ValueError:
        return None

    if not parts:
        return None
    return parts[0]


def _parse_imported_modules(py_file: Path) -> list[str]:
    tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
    imported: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module is not None:
                imported.append(node.module)

    return imported


def _is_cross_module_internal_import(importer_module: str, import_path: str) -> bool:
    if not import_path.startswith("src.modules."):
        return False

    parts = import_path.split(".")
    if len(parts) < 4:
        return False

    imported_module = parts[2]
    imported_layer = parts[3]

    return imported_module != importer_module and imported_layer == "internal"


def _module_dependency_graph() -> dict[str, set[str]]:
    graph: dict[str, set[str]] = defaultdict(set)

    for py_file in _iter_python_files(MODULES_DIR):
        importer_module = _module_name_from_path(py_file)
        if importer_module is None:
            continue

        graph.setdefault(importer_module, set())

        for import_path in _parse_imported_modules(py_file):
            if not import_path.startswith("src.modules."):
                continue

            parts = import_path.split(".")
            if len(parts) < 3:
                continue

            imported_module = parts[2]
            if imported_module != importer_module:
                graph[importer_module].add(imported_module)
                graph.setdefault(imported_module, set())

    return graph


def _find_cycle(graph: dict[str, set[str]]) -> list[str] | None:
    visited: set[str] = set()
    stack: set[str] = set()
    parent: dict[str, str] = {}

    def dfs(node: str) -> list[str] | None:
        visited.add(node)
        stack.add(node)

        for neighbor in graph.get(node, set()):
            if neighbor not in visited:
                parent[neighbor] = node
                cycle = dfs(neighbor)
                if cycle:
                    return cycle
            elif neighbor in stack:
                cycle = [neighbor]
                cur = node
                while cur != neighbor:
                    cycle.append(cur)
                    cur = parent[cur]
                cycle.append(neighbor)
                cycle.reverse()
                return cycle

        stack.remove(node)
        return None

    for node in graph:
        if node not in visited:
            found = dfs(node)
            if found:
                return found

    return None


def test_modules_do_not_import_other_modules_internal() -> None:
    violations: list[str] = []

    for py_file in _iter_python_files(MODULES_DIR):
        importer_module = _module_name_from_path(py_file)
        if importer_module is None:
            continue

        for import_path in _parse_imported_modules(py_file):
            if _is_cross_module_internal_import(importer_module, import_path):
                rel_path = py_file.relative_to(ROOT_DIR)
                violations.append(
                    f"{rel_path}: cross-module internal import is forbidden: {import_path}"
                )

    assert not violations, "\n".join(violations)


def test_modules_have_no_circular_dependency() -> None:
    graph = _module_dependency_graph()
    cycle = _find_cycle(graph)

    assert cycle is None, f"Circular dependency detected: {' -> '.join(cycle)}"


def test_shared_file_count_within_threshold() -> None:
    files = [
        path
        for path in SHARED_DIR.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    ]

    assert len(files) <= SHARED_FILE_THRESHOLD, (
        f"shared/ file count is {len(files)}, threshold is {SHARED_FILE_THRESHOLD}"
    )
