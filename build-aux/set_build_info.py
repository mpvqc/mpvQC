# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

import argparse
import os
import sys
from collections.abc import Mapping
from pathlib import Path

BUILD_INFO_PATH = Path("data/build-info.toml")


def render_build_info(existing_lines: list[str], *, tag: str, commit: str, is_release: bool, channel: str) -> list[str]:
    replacements = {
        "version": f'version = "{tag}"',
        "commit": f'commit = "{commit}"',
        "is_release": f"is_release = {'true' if is_release else 'false'}",
        "channel": f'channel = "{channel}"',
    }

    lines: list[str] = []
    in_application = False
    seen_application = False
    unreplaced = set(replacements)
    for raw in existing_lines:
        stripped = raw.strip()
        if stripped.startswith("["):
            in_application = stripped == "[application]"
            seen_application = seen_application or in_application
        key = stripped.split("=")[0].strip() if "=" in stripped else ""
        if in_application and key in replacements:
            line_ending = raw[len(raw.rstrip("\r\n")) :]
            lines.append(replacements[key] + line_ending)
            unreplaced.discard(key)
        else:
            lines.append(raw)

    if not seen_application:
        msg = 'Could not find "[application]" in build-info template'
        raise KeyError(msg)
    if unreplaced:
        msg = f'Could not find {", ".join(sorted(unreplaced))} in "[application]" table of build-info template'
        raise KeyError(msg)
    return lines


def determine_channel(env: Mapping[str, str]) -> str:
    return env.get("MPVQC_BUILD_CHANNEL", "")


def main() -> None:
    parser = argparse.ArgumentParser(description="Stamp version info into data/build-info.toml")
    parser.add_argument("--tag", required=True, help="Version to stamp")
    parser.add_argument("--commit", required=True, help="Commit id to stamp")
    parser.add_argument("--is-release", required=True, choices=("true", "false"), help="Whether HEAD is tagged")
    args = parser.parse_args()

    original = BUILD_INFO_PATH.read_text(encoding="utf-8").splitlines(keepends=True)

    try:
        updated = render_build_info(
            original,
            tag=args.tag,
            commit=args.commit,
            is_release=args.is_release == "true",
            channel=determine_channel(os.environ),
        )
    except KeyError as e:
        print(e.args[0], file=sys.stderr)
        sys.exit(1)

    if updated != original:
        BUILD_INFO_PATH.write_text("".join(updated), encoding="utf-8")


if __name__ == "__main__":
    main()
