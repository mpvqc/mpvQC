# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import shutil
import tempfile
import uuid
from pathlib import Path
from zipfile import ZipFile


def _temp_root() -> Path:
    # The parallel runner hands out the directories and deletes them once the processes are gone.
    configured = os.environ.get("MPVQC_TEST_TEMP_ROOT")
    if configured:
        root = Path(configured)
        root.mkdir(parents=True, exist_ok=True)
        return root
    return Path(tempfile.mkdtemp(prefix="mpvqc-qmltest-"))


FIXTURES_DIR = Path(__file__).parent / "fixtures"
TEMP_ROOT = _temp_root()
TEMP_SAVES_DIR = TEMP_ROOT / "saves"
TEMP_SAVES_DIR.mkdir()
WIZARD_FIXTURES_DIR = TEMP_ROOT / "wizard-fixtures"


def create_app_data_directory() -> Path:
    base = Path(tempfile.mkdtemp(prefix="paths-", dir=str(TEMP_ROOT)))
    shutil.copytree(FIXTURES_DIR / "portable-root", base, dirs_exist_ok=True)
    return base


def temp_save_path() -> Path:
    return TEMP_SAVES_DIR / f"qc_document_{uuid.uuid4().hex[:8]}.txt"


def create_complex_qc_document() -> Path:
    base = TEMP_ROOT / f"complex-{uuid.uuid4().hex[:8]}"
    base.mkdir()
    video = base / "video.mp4"
    sub1 = base / "track1.ass"
    sub2 = base / "track2.ass"
    for f in (video, sub1, sub2):
        f.touch()
    doc = base / "qc-complex.txt"
    doc.write_text(
        "[FILE]\n"
        f"path     : {video}\n"
        f"subtitle : {sub1}\n"
        f"subtitle : {sub2}\n"
        "\n"
        "[DATA]\n"
        "[00:00:10] [Translation] line1\n"
        "[00:01:20] [Spelling] line2\n",
        encoding="utf-8",
    )
    return doc


def create_video_only_qc_document() -> Path:
    base = TEMP_ROOT / f"video-only-{uuid.uuid4().hex[:8]}"
    base.mkdir()
    video = base / "video_only.mp4"
    video.touch()
    doc = base / "qc-video-only.txt"
    doc.write_text(
        f"[FILE]\npath     : {video}\n\n[DATA]\n[00:00:10] [Translation] line1\n",
        encoding="utf-8",
    )
    return doc


def create_multi_video_qc_documents() -> tuple[Path, Path]:
    base = TEMP_ROOT / f"multi-video-{uuid.uuid4().hex[:8]}"
    base.mkdir()
    video_a = base / "alpha.mp4"
    video_b = base / "beta.mp4"
    for f in (video_a, video_b):
        f.touch()
    doc_a = base / "qc-alpha.txt"
    doc_a.write_text(
        f"[FILE]\npath     : {video_a}\n\n[DATA]\n[00:00:10] [Translation] line1\n",
        encoding="utf-8",
    )
    doc_b = base / "qc-beta.txt"
    doc_b.write_text(
        f"[FILE]\npath     : {video_b}\n\n[DATA]\n[00:00:20] [Spelling] line2\n",
        encoding="utf-8",
    )
    return doc_a, doc_b


def file_contains(path: Path, text: str) -> bool:
    return path.is_file() and text in path.read_text(encoding="utf-8")


def backup_archive_any_entry_contains(backup_dir: Path, text: str) -> bool:
    if not backup_dir.is_dir():
        return False
    for archive in backup_dir.glob("*.zip"):
        with ZipFile(archive) as zf:
            for name in zf.namelist():
                if text in zf.read(name).decode("utf-8", errors="replace"):
                    return True
    return False
