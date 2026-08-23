# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Enforces the import rules of the feature slices."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

SLICES = ("appearance", "comments", "exporting", "importing", "window")
COMPOSITION_ROOTS = "mpvqc/injections.py and mpvqc/startup.py"
HELPERS = ("jobs",)
SHARED_ROLES = {"services": "services", "shared": "shared"}
MIN_EDGES_PER_SLICE = 20

HELD_ROOTS = ("linux", "windows")

SAME_SLICE = {
    "enums": {"shared"},
    "models": {"enums", "services", "shared"},
    "services": {"services", "shared"},
    "viewmodels": {"viewmodels", "models", "services", "enums", "shared"},
}

OTHER_SLICE = {
    "enums": {"shared"},
    "models": {"enums", "shared"},
    "services": {"services", "shared"},
    "viewmodels": {"services", "enums", "shared"},
}


def _module_name(path: Path) -> tuple[str, bool]:
    parts = path.relative_to(REPO).with_suffix("").parts
    is_package = parts[-1] == "__init__"
    if is_package:
        parts = parts[:-1]
    return ".".join(parts), is_package


def _resolve(importer: str, importer_is_package: bool, node: ast.ImportFrom) -> str:
    if node.level == 0:
        return node.module or ""
    parts = importer.split(".")
    drop = node.level - 1 if importer_is_package else node.level
    base = parts[: len(parts) - drop]
    return ".".join([*base, node.module]) if node.module else ".".join(base)


def _edges(path: Path):
    """Yield (target module, imported names, line) for every import statement in the file."""
    name, is_package = _module_name(path)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name, [alias.name], node.lineno
        elif isinstance(node, ast.ImportFrom):
            target = _resolve(name, is_package, node)
            names = [alias.name for alias in node.names]
            if node.module is None:
                for imported in names:
                    yield f"{target}.{imported}", [imported], node.lineno
            else:
                yield target, names, node.lineno


def _classify(target: str) -> tuple[str, str | None, str | None]:
    """Return (kind, slice, role); kind is slice | shared | helper | stdlib | external | unplaced."""
    parts = target.split(".")
    if parts[0] != "mpvqc":
        kind = "stdlib" if parts[0] in sys.stdlib_module_names else "external"
        return kind, None, None
    if len(parts) > 1 and parts[1] in SLICES:
        return "slice", parts[1], parts[2] if len(parts) > 2 else "root"
    if len(parts) > 1 and parts[1] in SHARED_ROLES:
        return "shared", "shared", SHARED_ROLES[parts[1]]
    if len(parts) > 1 and parts[1] in HELPERS:
        return "helper", None, None
    return "unplaced", None, None


def _held_root(target: str) -> str | None:
    parts = target.split(".")
    if len(parts) > 3 and parts[1] in SLICES and parts[3] in HELD_ROOTS:
        return ".".join(parts[:4])
    return None


def _role_root(target: str, kind: str) -> str:
    parts = target.split(".")
    if kind == "slice":
        return _held_root(target) or ".".join(parts[:3])
    return ".".join(parts[:2])


_EXPORT_CACHE: dict[str, set[str]] = {}


def _root_exports(root: str) -> set[str]:
    """Names the role root's __init__ binds; an export shadows a submodule of the same name."""
    if root not in _EXPORT_CACHE:
        init = REPO / Path(*root.split(".")) / "__init__.py"
        exports = set()
        if init.exists():
            for node in ast.parse(init.read_text(encoding="utf-8")).body:
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    exports.update(alias.asname or alias.name.split(".")[0] for alias in node.names)
        _EXPORT_CACHE[root] = exports
    return _EXPORT_CACHE[root]


def _reaches_past_role_root(target: str, kind: str, names: list[str]) -> bool:
    root = _role_root(target, kind)
    if root == "mpvqc.shared":
        return False
    if target != root:
        return True
    root_dir = REPO / Path(*root.split("."))
    return any(
        name not in _root_exports(root) and ((root_dir / f"{name}.py").exists() or (root_dir / name).is_dir())
        for name in names
    )


def _root_import_hint(target: str, kind: str, names: list[str]) -> str:
    root = _role_root(target, kind)
    if target == root:
        return f"it pulls the submodule {', '.join(names)} through the root; import names, not modules"
    return f"import {', '.join(names)} from {root} instead"


def _production_files(slice_: str) -> list[Path]:
    return sorted((REPO / "mpvqc" / slice_).rglob("*.py"))


def _feature_test_files(slice_: str) -> list[Path]:
    return sorted((REPO / "test" / slice_).rglob("*.py"))


def _role_root_files(slice_: str) -> list[Path]:
    return sorted((REPO / "mpvqc" / slice_).glob("*/__init__.py"))


def _role_of(path: Path) -> str | None:
    parts = _module_name(path)[0].split(".")
    return parts[2] if len(parts) > 2 else None


def _non_lattice_violation(where: str, role: str, kind: str, target: str) -> str | None:
    if kind == "helper" and role not in ("services", "viewmodels"):
        return f"{where}: {role} may not import {target}; the helpers under mpvqc/ are for services and view models"
    if kind == "unplaced":
        return (
            f"{where}: {target} has no row in the lattice yet; "
            f"classify it in {Path(__file__).name} before a slice uses it"
        )
    return None


def _lattice_violation(where: str, slice_: str, role: str, target: str, names: list[str]) -> str | None:
    kind, t_slice, t_role = _classify(target)
    if t_role == "root":
        return f"{where}: only the composition roots ({COMPOSITION_ROOTS}) import the slice root {target}"
    same_slice = kind == "slice" and t_slice == slice_
    if same_slice and t_role == role:
        return None
    allowed = SAME_SLICE[role] if same_slice else OTHER_SLICE[role]
    if t_role not in allowed:
        whose = (
            "its own slice" if same_slice else f"another slice ({t_slice})" if kind == "slice" else "the shared layer"
        )
        return (
            f"{where}: {role} may not import from the {t_role} of {whose}; "
            f"{role} may import: {', '.join(sorted(allowed))}"
        )
    if _reaches_past_role_root(target, kind, names):
        return (
            f"{where}: reaches past the role root {_role_root(target, kind)}; {_root_import_hint(target, kind, names)}"
        )
    return None


def check_production() -> list[str]:
    violations = []
    for slice_ in SLICES:
        for path in _production_files(slice_):
            role = _role_of(path)
            if path.name == "wiring.py" or role is None:
                continue
            for target, names, line in _edges(path):
                kind = _classify(target)[0]
                where = f"{path.relative_to(REPO)}:{line}"
                if kind in ("slice", "shared"):
                    violation = _lattice_violation(where, slice_, role, target, names)
                else:
                    violation = _non_lattice_violation(where, role, kind, target)
                if violation:
                    violations.append(violation)
    return violations


def check_feature_tests() -> list[str]:
    violations = []
    for slice_ in SLICES:
        for path in _feature_test_files(slice_):
            for target, names, line in _edges(path):
                kind, _, t_role = _classify(target)
                if kind not in ("slice", "shared") or t_role == "root":
                    continue
                if _reaches_past_role_root(target, kind, names):
                    violations.append(
                        f"{path.relative_to(REPO)}:{line}: the test reaches past the role root "
                        f"{_role_root(target, kind)}; {_root_import_hint(target, kind, names)}"
                    )
    return violations


def check_role_roots() -> list[str]:
    violations = []
    for slice_ in SLICES:
        for init in _role_root_files(slice_):
            root = _module_name(init)[0]
            for target, names, line in _edges(init):
                reached = [f"{root}.{name}" for name in names] if target == root else [target]
                held = {module for module in map(_held_root, reached) if module and module.startswith(f"{root}.")}
                violations.extend(
                    f"{init.relative_to(REPO)}:{line}: the role root re-exports the held root {module}; "
                    f"a held root answers for its own names, so drop the re-export and import them from there"
                    for module in sorted(held)
                )
    return violations


def check_wiring() -> list[str]:
    violations = []
    for slice_ in SLICES:
        path = REPO / "mpvqc" / slice_ / "wiring.py"
        name, is_package = _module_name(path)
        for node in ast.parse(path.read_text(encoding="utf-8")).body:
            if isinstance(node, ast.Import):
                targets = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                targets = [_resolve(name, is_package, node)]
            else:
                continue
            violations.extend(
                f"{path.relative_to(REPO)}:{node.lineno}: wiring imports {target} at module level, "
                f"which registers QML types before QGuiApplication exists; "
                f"import it inside the function that needs it"
                for target in targets
                if target.split(".")[0] in ("mpvqc", "PySide6")
            )
    return violations


def _fail_on(violations: list[str]) -> None:
    if violations:
        pytest.fail(f"{len(violations)} import rule violation(s):\n" + "\n".join(violations), pytrace=False)


def test_slices_follow_the_lattice_and_import_role_roots_only():
    _fail_on(check_production())


def test_feature_tests_import_role_roots_only():
    _fail_on(check_feature_tests())


def test_role_roots_re_export_no_held_root():
    _fail_on(check_role_roots())


def test_wiring_imports_no_mpvqc_and_no_qt_at_module_level():
    _fail_on(check_wiring())


@pytest.mark.parametrize("slice_", SLICES)
def test_the_production_scan_sees_the_slice(slice_: str):
    files = _production_files(slice_)
    edges = [edge for path in files for edge in _edges(path)]
    assert files, f"the production scan found no files under mpvqc/{slice_}"
    assert {_role_of(path) for path in files} - {None}, f"no file under mpvqc/{slice_} resolved to a role"
    assert len(edges) >= MIN_EDGES_PER_SLICE, f"the production scan read {len(edges)} imports under mpvqc/{slice_}"


@pytest.mark.parametrize("slice_", SLICES)
def test_the_feature_test_scan_sees_the_slice(slice_: str):
    files = _feature_test_files(slice_)
    edges = [edge for path in files for edge in _edges(path)]
    assert files, f"the feature test scan found no files under test/{slice_}"
    assert len(edges) >= MIN_EDGES_PER_SLICE, f"the feature test scan read {len(edges)} imports under test/{slice_}"


@pytest.mark.parametrize("slice_", SLICES)
def test_the_role_root_scan_sees_the_slice(slice_: str):
    files = _role_root_files(slice_)
    edges = [edge for path in files for edge in _edges(path)]
    assert files, f"the role root scan found no role __init__ under mpvqc/{slice_}"
    assert edges, f"the role root scan read no imports under mpvqc/{slice_}"
