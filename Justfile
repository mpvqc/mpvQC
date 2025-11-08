# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

export QT_QPA_PLATFORM := 'offscreen'
export QT_QUICK_CONTROLS_MATERIAL_VARIANT := 'Dense'
export QT_QUICK_CONTROLS_STYLE := 'Material'

alias fmt := format

@_default:
    just --list --unsorted

# Install dependencies and configure basic stuff
[group('dev')]
init ARGS='--group dev':
    #!/usr/bin/env bash
    uv sync {{ ARGS }}

    if [[ "{{ ARGS }}" == "--group dev" ]]; then
      QMLLS_INI=".qmlls.ini"
      echo "[General]" > "$QMLLS_INI"
      echo "DisableDefaultImports=false" >> "$QMLLS_INI"
      echo "no-cmake-calls=true" >> "$QMLLS_INI"
      echo "importPaths={{ justfile_directory() }}/pyobjects" >> "$QMLLS_INI"
      echo "buildDir={{ justfile_directory() }}" >> "$QMLLS_INI"
      echo "just init: Created $QMLLS_INI ..."

      echo "Created by command: just init" > portable
      echo "Runs application in portable mode by storing all files in the <git-repo>/appdata directory" >> portable
      echo "just init: Configured portable mode ..."

      mkdir -p appdata/export-templates
      cp data/config/backup-template.jinja appdata/export-templates/export-working.jinja
      echo '{{ '{{' }}' > appdata/export-templates/export-error.jinja
    fi

[group('dev')]
@format:
    uvx prek@0.2.12 run --all-files

[group('dev')]
update-python-dependencies:
    uv sync --upgrade
    just _update-dependency-versions

[group('dev')]
update-git-hook-dependencies:
    uvx prek@0.2.12 autoupdate

# Build full project into build/release
[group('build')]
@build: clean
    just build-develop
    mkdir -p build/release
    cp -r mpvqc build/release
    cp main.py build/release
    cp rc_project.py build/release

# Build and compile resources into source directory
[group('build')]
@build-develop: _update_pyproject_file
    uv run pyside6-project build

# Remove ALL generated files
[group('build')]
@clean:
    find i18n -name "*.qm" -type f -delete
    find qt/qml -name "*.qmlc" -type f -delete
    rm -rf build pyobjects test/rc_project.py rc_project.py project.json project.qrc

# Run Python and QML tests
[group('test')]
@test: _prepare-tests (test-python 'no-prep') (test-qml 'no-prep')

[group('test')]
test-python SKIP_PREPARATION='false':
    #!/usr/bin/env bash
    if [[ "{{ SKIP_PREPARATION }}" == "false" ]] then
      just _prepare-tests
    fi
    uv run pytest build-aux test

[group('test')]
test-qml SKIP_PREPARATION='false':
    #!/usr/bin/env bash
    if [[ "{{ SKIP_PREPARATION }}" == "false" ]] then
      just _prepare-tests
    fi
    uv run python -c '
    import sys
    from PySide6.QtQuickTest import QUICK_TEST_MAIN_WITH_SETUP
    from test.prepare_qml import MpvqcTestSetup

    # Pass additional arguments to qmltestrunner:
    sys.argv += ["-silent"]
    sys.argv += ["-input", "qt/qml"]
    # sys.argv += ["-eventdelay", "50"]  # Simulate slower systems

    ex = QUICK_TEST_MAIN_WITH_SETUP("qmltestrunner", MpvqcTestSetup, argv=sys.argv)
    sys.exit(ex)
    '

# Lint Python files (type checker only)
[group('lint')]
@lint-python:
    uvx pyrefly@0.39.4 check --ignore missing-attribute

# Lint QML files
[group('lint')]
@lint-qml: build-develop
    uv run pyside6-project qmllint

# Add language 'LOCALE' e.g. 'fr-FR' (ISO 639-1, ISO 3166-1)
[group('i18n')]
@add-translation LOCALE: _update_pyproject_file
    uv run pyside6-lupdate -source-language en-US -target-language {{ LOCALE }} -ts i18n/{{ LOCALE }}.ts
    just update-translations

# Update translation strings
[group('i18n')]
@update-translations: _update_pyproject_file _update_lupdate_project_file
    uv run pyside6-lupdate -locations none -project project.json

# Insert dependency versions
[group('CI')]
@insert-dependency-versions +UPDATE_INPLACE:
    uv --offline export \
        --no-hashes \
        --no-annotate \
        --output-file requirements.txt
    python build-aux/insert-dependency-versions.py \
        --requirements-txt requirements.txt \
        --update-inplace {{ UPDATE_INPLACE }}
    rm requirements.txt

@_prepare-tests: build-develop
    rm -f test/rc_project.py
    cp rc_project.py test/rc_project.py

@_update_pyproject_file: _generate-qrc-file
    uv run python build-aux/update_pyproject_file.py \
        --relative-to . \
        --include-directory qt/qml \
        --include-directory data \
        --include-directory mpvqc \
        --include-directory i18n \
        --include-file main.py \
        --include-file project.qrc

_generate-qrc-file:
    #!/usr/bin/env bash

    if [[ "${MPVQC_COMPILE_QML}" == "true" ]]; then
      echo "Compiling QML files to cache..."
      find qt/qml -name "*.qml" -not -name "tst_*.qml" -type f | while read qml_file; do
        qmlc_file="${qml_file}c"
        echo "  Compiling $(basename "$qml_file")..."
        uv run pyside6-qmlcachegen --only-bytecode "$qml_file" -o "$qmlc_file" || exit 1
      done
      echo "  Removing .aotstats files..."
      find qt/qml -name "*.aotstats" -type f -delete
      echo "QML compilation complete!"
    else
      echo "Skipping QML cache generation. Can be enabled by setting env var MPVQC_COMPILE_QML=true"
    fi

    uv run python build-aux/generate-qrc-file.py \
        --relative-to . \
        --include-directory qt/qml \
        --include-directory data \
        --include-directory i18n \
        --out-file project.qrc

@_update_lupdate_project_file:
    uv run python build-aux/generate-lupdate-project-file.py \
        --relative-to . \
        --include-directory qt/qml \
        --include-directory mpvqc \
        --include-directory i18n \
        --include-file main.py \
        --include-file project.qrc \
        --out-file project.json

# Update dependency versions in build-info.toml
_update-dependency-versions:
    #!/usr/bin/env bash
    uv --offline export --no-hashes --no-annotate | uv run python -c '
    import re, sys, tomllib
    from pathlib import Path

    # Parse versions from stdin
    versions = {}
    for line in sys.stdin:
        line = line.strip()
        if line and not line.startswith("#"):
            package_spec = line.split(";")[0].strip()
            if "==" in package_spec:
                package, version = package_spec.split("==", 1)
                versions[package.lower()] = version

    # Update build-info.toml
    toml_path = Path() / "data" / "build-info.toml"
    content = toml_path.read_text()

    with toml_path.open("rb") as f:
        data = tomllib.load(f)

    for dep_list in ["dependency", "dev_dependency"]:
        for dep in data[dep_list]:
            package_key = dep["package"].lower()
            if package_key in versions:
                v = versions[package_key]
                name_escaped = re.escape(dep["name"])
                pattern = "(name = \"" + name_escaped + "\".*?version = )\"[^\"]*\""
                replacement = r"\1" + "\"" + v + "\""
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    toml_path.write_text(content)
    '
