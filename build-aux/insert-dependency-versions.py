# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Requirement:
    name: str
    version: str


def parse_requirement(line: str) -> Requirement | None:
    """
    >>> parse_requirement("requests==2.25.1")
    requests==2.25.1
    Requirement(identifier='requests', version='2.25.1')

    >>> parse_requirement("# this is a comment")
    """

    if line.startswith("#"):
        return None

    name_version = line.split(";", maxsplit=1)[0].strip()
    name, version = name_version.split("==")

    return Requirement(name.strip(), version.strip())


class ArgumentValidator:
    _errors = []

    def validate_files(self, files: list[Path]):
        for file in files:
            self._validate_file(file)

    def _validate_file(self, file: Path):
        if not file.exists():
            self._errors.append(f"File {file} does not exist")
        elif not file.is_file():
            self._errors.append(f"File {file} is not a file")

    def require_files(self, files: list[Path], min_amount: int, requirement: str):
        if len(files) < min_amount:
            self._errors.append(f"Require at least {min_amount} {requirement}")

    def break_on_errors(self):
        if errors := self._errors:
            for error in errors:
                print(error, file=sys.stderr)
            sys.exit(1)


class RequirementsUpdater:
    """"""

    _replace_tag = "@@pypi-{name}@@"
    _validate_tag = "@@pypi-"

    _requirements: list[Requirement] = []

    def parse(self, requirements_txt: Path):
        requirements_lines = requirements_txt.read_text(encoding="utf-8").splitlines()

        for line in requirements_lines:
            if requirement := parse_requirement(line):
                self._requirements.append(requirement)

    def replace_in_files(self, files: list[Path]):
        for file in files:
            text = file.read_text(encoding="utf-8")
            for requirement in self._requirements:
                search = self._replace_tag.format(name=requirement.name)
                text = text.replace(search, requirement.version)
            file.write_text(text, encoding="utf-8", newline="\n")

    def validate(self, files: list[Path]):
        error = False
        for file in files:
            for index, line in enumerate(file.read_text(encoding="utf-8").splitlines(keepends=False)):
                if self._validate_tag in line:
                    error = True
                    print(f"Unresolved versions in {file}:{index + 1}:{line}", file=sys.stderr)
        if error:
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Work with dependencies from a pyproject.toml file")
    parser.add_argument(
        "--requirements-txt",
        type=str,
        required=True,
        help="requirements.txt file",
    )
    parser.add_argument(
        "--update-inplace",
        type=str,
        nargs="+",
        help="file to update versions inplace",
    )

    args = parser.parse_args()
    run_insert(args)


def run_insert(args):
    requirements_txt = Path(args.requirements_txt)
    source_files = [Path(path).absolute() for path in args.update_inplace]

    validator = ArgumentValidator()
    validator.validate_files([requirements_txt, *source_files])
    validator.require_files(source_files, min_amount=1, requirement="file(s) to write dependency versions to")
    validator.break_on_errors()

    updater = RequirementsUpdater()
    updater.parse(requirements_txt)
    updater.replace_in_files(source_files)
    updater.validate(source_files)


if __name__ == "__main__":
    main()
