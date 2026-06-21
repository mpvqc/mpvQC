# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

import re
import sys
import tomllib
from pathlib import Path

BUILD_INFO = Path("data") / "build-info.toml"
DEPENDENCY_TABLES = ("dependency", "dev_dependency")


def parse_versions(exported: str) -> dict[str, str]:
    versions: dict[str, str] = {}
    for raw in exported.splitlines():
        spec = raw.split(";", 1)[0].strip()
        if spec.startswith("#"):
            continue
        package, separator, version = spec.partition("==")
        if separator:
            versions[package.lower()] = version
    return versions


def update_versions(content: str, versions: dict[str, str]) -> str:
    data = tomllib.loads(content)
    for table in DEPENDENCY_TABLES:
        for dependency in data.get(table, []):
            name: str = dependency["name"]
            package: str = dependency["package"]
            version = versions.get(package.lower())
            if version is None:
                continue
            pattern = r'(name = "' + re.escape(name) + r'".*?version = )"[^"]*"'
            content = re.sub(pattern, lambda match, v=version: f'{match.group(1)}"{v}"', content, flags=re.DOTALL)
    return content


def main() -> None:
    versions = parse_versions(sys.stdin.read())
    content = BUILD_INFO.read_text(encoding="utf-8")
    updated = update_versions(content, versions)
    if updated != content:
        BUILD_INFO.write_text(updated, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
