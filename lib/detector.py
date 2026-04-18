"""Auto-detect the iOS app folder name from an Xcode project."""

from __future__ import annotations

from pathlib import Path


def detect_app_name(root: Path) -> str:
    """Return the app name based on a single .xcodeproj/.xcworkspace under root.

    Falls back to .xcworkspace if no .xcodeproj is present. Raises SystemExit
    with an actionable message when zero or multiple candidates are found.
    """
    candidates = sorted({p.stem for p in root.glob("*.xcodeproj")})
    if not candidates:
        candidates = sorted({p.stem for p in root.glob("*.xcworkspace")})
    if not candidates:
        raise SystemExit(
            f"Could not auto-detect the app name: no .xcodeproj or .xcworkspace "
            f"found in {root}. Pass --app-name explicitly."
        )
    if len(candidates) > 1:
        raise SystemExit(
            f"Multiple Xcode projects found ({', '.join(candidates)}). "
            "Pass --app-name to choose one."
        )
    return candidates[0]
