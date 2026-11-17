"""Safe handling of uploaded source archives: streaming the upload to disk with a size cap, and
extracting a zip without path traversal, symlinks or zip bombs."""

from __future__ import annotations

import re
import shutil
import stat
import zipfile
from pathlib import Path, PurePosixPath
from typing import BinaryIO

CHUNK = 1024 * 1024
_IGNORED_TOP_LEVEL = {"__MACOSX"}


class ArchiveError(ValueError):
    """The archive is invalid, unsafe or too large."""


class UploadTooLarge(ArchiveError):
    pass


def safe_folder_name(filename: str | None, fallback: str = "source") -> str:
    """A folder name from an upload's file name: its stem, reduced to safe characters.

    The reviewer derives its run ID from the target folder's name, so this keeps the name readable."""
    stem = re.split(r"[\\/]", filename or "")[-1]
    if stem.lower().endswith(".zip"):
        stem = stem[:-4]
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-.")
    return stem[:64] or fallback


def save_upload(stream: BinaryIO, dest: Path, max_bytes: int) -> int:
    """Copy an upload stream to `dest`, stopping with UploadTooLarge past `max_bytes`."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with dest.open("wb") as out:
        while True:
            chunk = stream.read(CHUNK)
            if not chunk:
                break
            written += len(chunk)
            if written > max_bytes:
                raise UploadTooLarge(f"the upload is larger than the {max_bytes // (1024 * 1024)} MB limit")
            out.write(chunk)
    return written


def _member_path(name: str) -> PurePosixPath | None:
    """The member's relative path, or None for a directory entry. Raises on an unsafe path."""
    normalized = name.replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        raise ArchiveError(f"the archive holds an absolute path: {name!r}")
    parts = [p for p in normalized.split("/") if p not in ("", ".")]
    if any(p == ".." for p in parts):
        raise ArchiveError(f"the archive holds a path outside its folder: {name!r}")
    if not parts or normalized.endswith("/"):
        return None
    return PurePosixPath(*parts)


def _is_symlink(info: zipfile.ZipInfo) -> bool:
    return stat.S_ISLNK(info.external_attr >> 16)


def extract_zip(zip_path: Path, dest: Path, max_bytes: int, max_files: int) -> Path:
    """Extract `zip_path` into `dest` and return the directory to review.

    When the archive holds a single top-level folder (the usual result of zipping a folder), that folder
    is returned, so the review is named after it."""
    if not zipfile.is_zipfile(zip_path):
        raise ArchiveError("the upload is not a zip archive")
    dest.mkdir(parents=True, exist_ok=True)
    dest_resolved = dest.resolve()
    with zipfile.ZipFile(zip_path) as zf:
        infos = zf.infolist()
        files = []
        for info in infos:
            rel = _member_path(info.filename)
            if rel is None:
                continue
            if _is_symlink(info):
                raise ArchiveError(f"the archive holds a symbolic link: {info.filename!r}")
            files.append((info, rel))
        if not files:
            raise ArchiveError("the archive holds no files")
        if len(files) > max_files:
            raise ArchiveError(f"the archive holds {len(files)} files; the limit is {max_files}")
        declared = sum(i.file_size for i, _ in files)
        if declared > max_bytes:
            raise ArchiveError(f"the archive expands to {declared // (1024 * 1024)} MB; "
                               f"the limit is {max_bytes // (1024 * 1024)} MB")
        total = 0
        for info, rel in files:
            target = (dest / Path(*rel.parts)).resolve()
            if dest_resolved not in target.parents:
                raise ArchiveError(f"the archive holds a path outside its folder: {info.filename!r}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, target.open("wb") as out:
                while True:
                    chunk = src.read(CHUNK)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > max_bytes:  # sizes in the header can lie
                        raise ArchiveError(f"the archive expands past the {max_bytes // (1024 * 1024)} MB limit")
                    out.write(chunk)
    return review_root(dest)


def review_root(dest: Path) -> Path:
    entries = [p for p in dest.iterdir() if p.name not in _IGNORED_TOP_LEVEL]
    if len(entries) == 1 and entries[0].is_dir():
        return entries[0]
    return dest


def remove_tree(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)
