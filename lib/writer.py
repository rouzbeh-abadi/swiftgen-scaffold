"""Filesystem helpers used by the scaffolder.

All helpers take a project-relative path plus a base directory so the
action log they return is always rooted at the project, regardless of the
caller's current working directory. When dry_run is True, no filesystem
changes are made — the helpers return a "would …" status line so the
caller can preview actions safely.
"""

from __future__ import annotations

from pathlib import Path


def write_file(
    rel_path: str,
    content: str,
    base: Path,
    force: bool,
    only_if_missing: bool = False,
    dry_run: bool = False,
) -> str:
    """Write content to base/rel_path, creating parents as needed.

    - If the file exists and only_if_missing is True, leave it alone.
    - If the file exists and force is False, leave it alone.
    - When dry_run is True, no filesystem changes are made.
    - Otherwise, write the content.
    """
    abs_path = base / rel_path
    if abs_path.exists():
        if only_if_missing or not force:
            return f"  skip   {rel_path}  (exists)"
    if dry_run:
        return f"  would-write  {rel_path}"
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text(content, encoding="utf-8")
    return f"  write  {rel_path}"


def ensure_dir(rel_path: str, base: Path, dry_run: bool = False) -> str:
    """Create base/rel_path (and parents) if missing. Idempotent.

    When dry_run is True, no filesystem changes are made.
    """
    abs_path = base / rel_path
    if abs_path.exists():
        return f"  exists {rel_path}/"
    if dry_run:
        return f"  would-mkdir  {rel_path}/"
    abs_path.mkdir(parents=True, exist_ok=True)
    return f"  mkdir  {rel_path}/"
