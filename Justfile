# Copyright 2024
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

export QML_IMPORT_PATH := 'qml'
export QT_QPA_PLATFORM := 'offscreen'
export QT_QUICK_CONTROLS_MATERIAL_VARIANT := 'Dense'
export QT_QUICK_CONTROLS_STYLE := 'Material'

@_default:
    just --list

# Format code
@format:
    uv run pre-commit run --all-files

# Initialize repository
init ARGS='--group dev':
    #!/usr/bin/env bash
    uv sync {{ ARGS }}

    if [[ "{{ ARGS }}" == "--group dev" ]] then
      echo "Created by command: just init" > portable
      echo "Runs application in portable mode by storing all files in the <git-repo>/appdata directory" >> portable

      mkdir -p appdata/export-templates
      cp data/config/backup-template.jinja appdata/export-templates/export-working.jinja
      echo '{{ '{{' }}' > appdata/export-templates/export-error.jinja
    fi

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
@clean: _update_pyproject_file
    uv run pyside6-project clean
    rm -rf build test/rc_project.py project.json project.qrc

# Add language; pattern: language-region ISO 639-1, ISO 3166-1; example: fr-FR
[group('i18n')]
@add-translation locale: _update_pyproject_file
    uv run pyside6-lupdate -source-language en-US -target-language {{ locale }} -ts i18n/{{ locale }}.ts
    just update-translations

# Update *.ts files by traversing the source code
[group('i18n')]
@update-translations: _update_pyproject_file _update_lupdate_project_file
    uv run pyside6-lupdate -locations none -project project.json

# Lint QML files
[group('lint')]
@lint-qml: build-develop
    pyside6-project qmllint

# Run Python and QML tests
[group('test')]
@test: test-python test-qml

# Run Python tests
[group('test')]
@test-python: build-develop
    rm -f test/rc_project.py
    cp rc_project.py test/rc_project.py
    uv run pytest build-aux test

# Run QML tests
[group('test')]
@test-qml: build-develop
    uv run test/test_qml.py -silent -input qt/qml

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

@_update_pyproject_file: _generate-qrc-file
    uv run python build-aux/update_pyproject_file.py \
        --relative-to . \
        --include-directory qt/qml \
        --include-directory data \
        --include-directory mpvqc \
        --include-directory i18n \
        --include-file main.py \
        --include-file project.qrc

@_generate-qrc-file:
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
