# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Runs the QML test files, one process per file, several at a time.

Qt Quick Test itself has no parallel mode: a run takes a single `-input` path and walks it in order.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

QML_ROOT = Path("qt/qml")
TOTALS_PATTERN = re.compile(r"^Totals: (\d+) passed", re.MULTILINE)
INTERRUPTED_EXIT_CODE = 130


@dataclass(frozen=True)
class ShardResult:
    file: Path
    passed: bool
    tests: int
    seconds: float
    output: str


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="testqml.runner")
    parser.add_argument(
        "--jobs",
        default="auto",
        help="Number of test files to run at once, or 'auto'. One job runs everything in a single process.",
    )
    return parser.parse_args()


def resolve_jobs(requested: str, shard_count: int, platform: str = sys.platform) -> int:
    wanted = _requested_jobs(requested, shard_count)
    if platform == "win32" and wanted > 1:
        # Windows drives real windows, which would fight over the keyboard focus.
        print("Windows runs the test files one after another, in a single process", flush=True)
        return 1
    return wanted


def _requested_jobs(requested: str, shard_count: int) -> int:
    if requested == "auto":
        return min(os.process_cpu_count() or 1, shard_count)
    if not requested.isdigit() or int(requested) < 1:
        msg = f"--jobs takes 'auto' or a number of at least 1, got '{requested}'"
        raise SystemExit(msg)
    return min(int(requested), shard_count)


def discover_test_files() -> list[Path]:
    # Biggest first, because the longest file decides the wall time.
    files = sorted(QML_ROOT.rglob("tst_*.qml"), key=lambda file: file.stat().st_size, reverse=True)
    if not files:
        msg = f"No test files found below '{QML_ROOT}'"
        raise SystemExit(msg)
    return files


def count_tests(output: str) -> int:
    return sum(int(match.group(1)) for match in TOTALS_PATTERN.finditer(output))


def run_shard(file: Path, temp_root: Path) -> ShardResult:
    started = time.monotonic()
    process = subprocess.run(
        [sys.executable, "-m", "testqml.main", "--silent", "--target", str(file)],
        capture_output=True,
        text=True,
        check=False,
        env=os.environ | {"MPVQC_TEST_TEMP_ROOT": str(temp_root)},
    )
    output = process.stdout + process.stderr
    tests = count_tests(output)
    return ShardResult(
        file=file,
        # A run whose tests never started still reports success.
        passed=process.returncode == 0 and tests > 0,
        tests=tests,
        seconds=time.monotonic() - started,
        output=output,
    )


def run_in_single_process() -> int:
    return subprocess.run([sys.executable, "-m", "testqml.main"], check=False).returncode


def run_in_parallel(files: list[Path], jobs: int) -> int:
    print(f"Running {len(files)} test files, {jobs} at a time", flush=True)
    started = time.monotonic()
    run_root = Path(tempfile.mkdtemp(prefix="mpvqc-qmltest-"))
    results: list[ShardResult] = []
    interrupted = False

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures: list[Future[ShardResult]] = [
            pool.submit(run_shard, file, run_root / f"{index:02d}-{file.stem}") for index, file in enumerate(files)
        ]
        try:
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                marker = "PASS" if result.passed else "FAIL"
                print(f"{marker}  {result.seconds:6.1f}s  {result.file.name}", flush=True)
        except KeyboardInterrupt:
            interrupted = True
            for future in futures:
                future.cancel()

    if interrupted:
        shutil.rmtree(run_root, ignore_errors=True)
        print("\nInterrupted", flush=True)
        return INTERRUPTED_EXIT_CODE

    failures = [result for result in results if not result.passed]
    for failure in failures:
        print(f"\n{'=' * 80}\n{failure.file}\n{'=' * 80}\n{failure.output}", flush=True)

    tests = sum(result.tests for result in results)
    passed = len(results) - len(failures)
    elapsed = time.monotonic() - started
    print(f"\n{tests} tests, {passed} of {len(files)} files passed in {elapsed:.1f}s", flush=True)

    if not failures:
        shutil.rmtree(run_root, ignore_errors=True)
        return 0

    print(f"Test data of this run is in {run_root}\n\nRe-run the failed files one by one:", flush=True)
    for failure in failures:
        print(f"  just test-qml-debug {failure.file.stem}", flush=True)
    return 1


def main() -> int:
    args = parse_cli()
    files = discover_test_files()
    jobs = resolve_jobs(args.jobs, len(files))
    if jobs == 1:
        return run_in_single_process()
    return run_in_parallel(files, jobs)


if __name__ == "__main__":
    sys.exit(main())
