# MIT
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import json
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import sys
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements


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

    _requirements = []
    _resolved_requirements = []

    @dataclass
    class Requirement:
        name: str
        requirement: str  # either >=, ==, <=
        version: str

    @dataclass
    class ResolvedRequirement:
        name: str
        version: str

    def parse(self, requirements_file: Path):
        for requirement in parse_requirements(f"{requirements_file}", session=PipSession()):
            name_requirement_version = requirement.requirement.split(";")[0]
            name, requirement, version = re.split("(>=|==|<=)", name_requirement_version)
            self._requirements.append(self.Requirement(name, requirement, version))

    def resolve_required_versions(self):
        for requirement in self._requirements:
            name = requirement.name
            if requirement.requirement == "==":
                resolved = self.ResolvedRequirement(name, requirement.version)
            elif requirement.requirement == ">=":
                with urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=5) as connection:
                    text = connection.read().decode("utf-8").strip()
                version = f"{json.loads(text)['info']['version']}".strip()
                resolved = self.ResolvedRequirement(name, version)
            else:
                raise f"Cannot resolve version for dependency '{name}' with requirement: {requirement.requirement}"
            self._resolved_requirements.append(resolved)

    def replace_in_files(self, files: list[Path]):
        for file in files:
            text = file.read_text(encoding="utf-8")
            for requirement in self._resolved_requirements:
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
    parser = argparse.ArgumentParser(description="Set dependency versions based on a requirements.txt file")
    parser.add_argument("--requirements", type=str, required=True, help="requirements.txt file")
    parser.add_argument(
        "--update-inplace", type=str, action="append", default=[], help="file to update versions inplace"
    )
    run(parser.parse_args())


def run(args):
    requirements = Path(args.requirements).absolute()
    source_files = [Path(path).absolute() for path in args.update_inplace]

    validator = ArgumentValidator()
    validator.validate_files([requirements, *source_files])
    validator.require_files(source_files, min_amount=1, requirement="file(s) to write dependency versions to")
    validator.break_on_errors()

    updater = RequirementsUpdater()
    updater.parse(requirements)
    updater.resolve_required_versions()
    updater.replace_in_files(source_files)
    updater.validate(source_files)


if __name__ == "__main__":
    main()
