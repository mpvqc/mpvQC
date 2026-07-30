# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

"""Drop-in replacement for `pyside6-project build`.

The stock tool spawns one `pyside6-metaobjectdump` subprocess per Python file
just to detect QML decorators, paying full interpreter startup each time.
This driver runs the same (pure stdlib) parser in-process instead and builds
independent files concurrently.

The PySide6 tooling modules live outside any package root, so they are located
and imported at runtime and the type checker cannot see into them.
"""

import importlib
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import PySide6

sys.path.insert(0, str(Path(PySide6.__file__).parent / "scripts"))

metaobjectdump = importlib.import_module("metaobjectdump")
pyside_project = importlib.import_module("project")
project_data = importlib.import_module("project_lib.project_data")

# The visitor appends project classes to the context's list, which aliases the
# module-level QOBJECT_DERIVED. Snapshot it so every file starts from the same
# baseline, exactly like the one-subprocess-per-file original.
_BASE_QOBJECT_DERIVED = tuple(metaobjectdump.QOBJECT_DERIVED)


def _check_qml_decorators(py_file: Path) -> tuple[bool, Any]:
    context = metaobjectdump.VisitorContext()
    context.qobject_derived = list(_BASE_QOBJECT_DERIVED)
    try:
        data = metaobjectdump.parse_file(py_file, context, suppress_file=True)
    except Exception as e:  # ruff: ignore[blind-except]
        print(f"{type(e).__name__}: parsing {py_file}: {e}", file=sys.stderr)
        sys.exit(1)

    qml_project_data = project_data.QmlProjectData()
    if not data:
        return False, qml_project_data

    has_class = project_data._has_qml_decorated_class(data["classes"])
    if has_class:
        if v := data.get(metaobjectdump.QML_IMPORT_NAME):
            qml_project_data.import_name = v
        if v := data.get(metaobjectdump.QML_IMPORT_MAJOR_VERSION):
            qml_project_data.import_major_version = v
            qml_project_data.import_minor_version = data.get(metaobjectdump.QML_IMPORT_MINOR_VERSION)
        if v := data.get(metaobjectdump.QT_MODULES):
            qml_project_data.qt_modules = v
    return has_class, qml_project_data


class FastBuildProject(pyside_project.Project):
    def _qml_module_check(self) -> None:
        """Like the base version, but detects decorators in-process."""
        if not self.cl_options.qml_module and not self.project.qml_files:
            return
        for file in self.project.files:
            if pyside_project.is_python_file(file):
                has_class, data = _check_qml_decorators(file)
                if has_class:
                    self._qml_module_sources.append(file)
                    if data:
                        self._qml_project_data = data

        if not self._qml_module_sources:
            return
        if not self._qml_project_data:
            print("Detected QML-decorated files, but was unable to detect QML_IMPORT_NAME")
            sys.exit(1)

        self._qml_module_dir = self.project.project_file.parent
        for uri_dir in self._qml_project_data.import_name.split("."):
            self._qml_module_dir /= uri_dir
        print(self._qml_module_dir)
        self._qml_dir_file = self._qml_module_dir / pyside_project.QMLDIR_FILE

        if not self.cl_options.quiet:
            count = len(self._qml_module_sources)
            print(f"{self.project.project_file.name}, {count} QML file(s), {self._qml_project_data}")

    def build(self) -> None:
        """Like the base version, but runs independent per-file build commands concurrently.

        Files are independent of each other (the py -> json -> qmltypes chain stays
        serial inside one _build_file call); only .qrc files may depend on other
        generated files, so they run last, serially.
        """
        for sub_project_file in self.project.sub_projects_files:
            FastBuildProject(project_file=sub_project_file).build()

        if self._qml_module_dir:
            self._qml_module_dir.mkdir(exist_ok=True, parents=True)

        sources = pyside_project._sort_sources(self.project.files)
        with ThreadPoolExecutor() as pool:
            futures = [pool.submit(self._build_file, f) for f in sources if f.suffix != ".qrc"]
            for future in futures:
                future.result()
        for file in sources:
            if file.suffix == ".qrc":
                self._build_file(file)

        if pyside_project.DesignStudioProject.is_ds_project(self.project.main_file):
            self.build_design_studio_resources()

        self._regenerate_qmldir()

    def _regenerate_qmldir(self) -> None:
        """Like the base version, but sorts the typeinfo lines.

        The original relies on glob() order, which reflects file creation order and
        turns nondeterministic once the build runs in parallel.
        """
        if self.cl_options.dry_run or not self._qml_dir_file:
            return
        if self.cl_options.force or pyside_project.requires_rebuild(self._qml_module_sources, self._qml_dir_file):
            with self._qml_dir_file.open("w") as qf:
                qf.write(f"module {self._qml_project_data.import_name}\n")
                for f in sorted(self._qml_module_dir.glob("*.qmltypes")):
                    qf.write(f"typeinfo {f.name}\n")


def main() -> None:
    pyside_project.ClOptions(dry_run=False, quiet=False, force=False, qml_module=False)
    try:
        project_file = pyside_project.resolve_valid_project_file(None)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    FastBuildProject(project_file).build()


if __name__ == "__main__":
    main()
