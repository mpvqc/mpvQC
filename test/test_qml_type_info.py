# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import ast
from collections import defaultdict
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# Every Python source the build hands to the type-info generator, whose output shares one flat folder.
BUILT_SOURCES = (REPO_ROOT / "main.py", REPO_ROOT / "mpvqc", REPO_ROOT / "testqml")

# The decorators PySide6's type-info generator reads as a QML registration. Matched by name in either
# form, wider than upstream on purpose: upstream takes some only bare and some only called, and a form
# it starts reading later must not slip past. A dotted or aliased decorator is invisible to the
# generator, so it is invisible here too.
QML_REGISTRATION_DECORATORS = frozenset(
    {
        "QmlAnonymous",
        "QmlAttached",
        "QmlElement",
        "QmlExtended",
        "QmlForeign",
        "QmlNamedElement",
        "QmlSingleton",
        "QmlUncreatable",
    }
)

DECORATOR_FORMS = [f"@{name}" for name in sorted(QML_REGISTRATION_DECORATORS)] + [
    f'@{name}("argument")' for name in sorted(QML_REGISTRATION_DECORATORS)
]


def decorator_name(decorator: ast.expr) -> str:
    match decorator:
        case ast.Name(id=name) | ast.Call(func=ast.Name(id=name)):
            return name
        case _:
            return ""


def registers_qml_type(module: Path) -> bool:
    tree = ast.parse(module.read_text(encoding="utf-8"))
    return any(
        decorator_name(decorator) in QML_REGISTRATION_DECORATORS
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
        for decorator in node.decorator_list
    )


def collect_registered_modules(*sources: Path) -> dict[str, list[Path]]:
    """Keyed by the type-info file each module claims, which is the module's own file name."""
    modules: list[Path] = []
    for source in sources:
        modules.extend(source.rglob("*.py") if source.is_dir() else [source])

    claims: dict[str, list[Path]] = defaultdict(list)
    for module in sorted(modules):
        if registers_qml_type(module):
            claims[module.stem].append(module)
    return dict(claims)


def write_module(directory: Path, relative_path: str, source: str) -> Path:
    module = directory / relative_path
    module.parent.mkdir(parents=True, exist_ok=True)
    module.write_text(source, encoding="utf-8")
    return module


@pytest.fixture(scope="module")
def registered_modules() -> dict[str, list[Path]]:
    return collect_registered_modules(*BUILT_SOURCES)


@pytest.mark.parametrize("decorator", DECORATOR_FORMS)
def test_collects_module_registering_qml_type(tmp_path, decorator):
    write_module(tmp_path, "footer.py", f"{decorator}\nclass MpvqcFooterViewModel: ...\n")

    assert collect_registered_modules(tmp_path).keys() == {"footer"}


@pytest.mark.parametrize("decorator", ["@dataclass", "@QtQml.QmlElement"])
def test_skips_module_without_registered_class(tmp_path, decorator):
    write_module(tmp_path, "domain.py", f"{decorator}\nclass Comment: ...\n")

    assert collect_registered_modules(tmp_path) == {}


def test_groups_modules_claiming_the_same_type_info_file(tmp_path):
    source = "@QmlElement\nclass MpvqcFooterViewModel: ...\n"
    importing = write_module(tmp_path, "importing/footer.py", source)
    viewmodels = write_module(tmp_path, "viewmodels/footer.py", source)

    assert collect_registered_modules(tmp_path) == {"footer": [importing, viewmodels]}


def test_scan_finds_the_modules_registered_today(registered_modules):
    """A scan that finds nothing would let the uniqueness test pass silently."""
    assert {"app", "bridge", "footer", "palette", "wizard"} <= registered_modules.keys()


def test_registered_modules_claim_distinct_type_info_files(registered_modules):
    collisions = {stem: modules for stem, modules in registered_modules.items() if len(modules) > 1}
    reported = "\n".join(
        f"{stem}.qmltypes <- " + ", ".join(str(module.relative_to(REPO_ROOT)) for module in modules)
        for stem, modules in collisions.items()
    )

    assert not collisions, f"modules writing the same type-info file, so one overwrites the other:\n{reported}"
