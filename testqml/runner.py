# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Runs the QML test files, one process per file, several at a time.

Qt Quick Test itself has no parallel mode: a run takes a single `-input` path and walks it in order.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

QML_ROOT = Path("qt/qml")
TOTALS_PATTERN = re.compile(r"^Totals: (\d+) passed", re.MULTILINE)
INTERRUPTED_EXIT_CODE = 130
_TERMINATE_TIMEOUT_SECONDS = 5.0


@dataclass(frozen=True)
class ShardResult:
    file: Path
    passed: bool
    tests: int
    seconds: float
    output: str


class ProcessTracker:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._active: set[subprocess.Popen[str]] = set()
        self._cancelled = False

    def run(self, command: list[str], *, env: dict[str, str]) -> tuple[int, str] | None:
        with self._lock:
            if self._cancelled:
                return None
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                errors="replace",
                env=env,
            )
            self._active.add(process)
        try:
            output, _ = process.communicate()
        finally:
            with self._lock:
                self._active.discard(process)
        return process.returncode, output

    def cancel_all(self) -> None:
        with self._lock:
            self._cancelled = True
            running = list(self._active)
        for process in running:
            _terminate_process(process)


def _terminate_process(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=_TERMINATE_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


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


def _run_passed(returncode: int, tests: int) -> bool:
    # A run whose tests never started still reports success.
    return returncode == 0 and tests > 0


def run_shard(file: Path, temp_root: Path, tracker: ProcessTracker | None = None) -> ShardResult:
    started = time.monotonic()
    active_tracker = tracker if tracker is not None else ProcessTracker()
    outcome = active_tracker.run(
        [sys.executable, "-m", "testqml.main", "--silent", "--target", str(file)],
        env=os.environ | {"MPVQC_TEST_TEMP_ROOT": str(temp_root)},
    )
    if outcome is None:
        return ShardResult(file=file, passed=False, tests=0, seconds=time.monotonic() - started, output="")

    returncode, output = outcome
    tests = count_tests(output)
    return ShardResult(
        file=file,
        passed=_run_passed(returncode, tests),
        tests=tests,
        seconds=time.monotonic() - started,
        output=output,
    )


def run_in_single_process() -> int:
    run_root = Path(tempfile.mkdtemp(prefix="mpvqc-qmltest-"))
    process = subprocess.Popen(
        [sys.executable, "-m", "testqml.main"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        errors="replace",
        env=os.environ | {"MPVQC_TEST_TEMP_ROOT": str(run_root)},
    )
    chunks: list[str] = []
    try:
        if process.stdout is not None:
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                chunks.append(line)
        returncode = process.wait()
    except KeyboardInterrupt:
        _terminate_process(process)
        shutil.rmtree(run_root, ignore_errors=True)
        print("\nInterrupted", flush=True)
        return INTERRUPTED_EXIT_CODE

    tests = count_tests("".join(chunks))
    if _run_passed(returncode, tests):
        shutil.rmtree(run_root, ignore_errors=True)
        return 0

    if returncode == 0 and tests == 0:
        print("No QML tests were executed", flush=True)
    print(f"Test data of this run is in {run_root}", flush=True)
    return returncode if returncode != 0 else 1


def run_in_parallel(files: list[Path], jobs: int) -> int:
    print(f"Running {len(files)} test files, {jobs} at a time", flush=True)
    started = time.monotonic()
    run_root = Path(tempfile.mkdtemp(prefix="mpvqc-qmltest-"))
    tracker = ProcessTracker()
    results: list[ShardResult] = []
    interrupted = False

    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures: list[Future[ShardResult]] = [
            pool.submit(run_shard, file, run_root / f"{index:02d}-{file.stem}", tracker)
            for index, file in enumerate(files)
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
            # ThreadPoolExecutor.__exit__ waits for running workers, so terminate active shards now.
            tracker.cancel_all()

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
