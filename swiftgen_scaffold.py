#!/usr/bin/env python3
"""Scaffold SwiftGen into an iOS Xcode project.

Run the script, paste your iOS project path when prompted, and the
scaffolder writes swiftgen.yml, the stencils, and the folders SwiftGen
needs — all inside the project you pointed at.

    python3 swiftgen_scaffold.py [--app-name NAME] [--force] [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from lib.detector import detect_app_name
from lib.templates import (
    LOCALIZABLE_PLACEHOLDER,
    SWIFTGEN_YML_TEMPLATE,
    XCASSETS_CONTENTS_JSON,
)
from lib.writer import ensure_dir, write_file

SCRIPT_DIR = Path(__file__).resolve().parent
STENCILS_DIR = SCRIPT_DIR / "stencils"


def prompt_for_project_path() -> Path:
    """Ask the user to paste the iOS project's absolute path.

    Strips surrounding whitespace and quotes so a path pasted from `pwd`
    works whether or not the shell wrapped it. An empty answer falls back
    to the current working directory.
    """
    print()
    print("Tip: in your iOS project's Terminal, run `pwd` and copy the path.")
    print("Press Enter to use the current directory.")
    print()
    raw = input("Project path: ").strip().strip("'\"")
    if not raw:
        return Path.cwd()
    return Path(raw).expanduser().resolve()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold SwiftGen into an iOS project. Prompts for the project path.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--app-name",
        help="App folder name. Auto-detected from .xcodeproj if omitted.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing swiftgen.yml and stencil templates.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview every action without writing anything to disk.",
    )
    args = parser.parse_args()

    project_root = prompt_for_project_path()
    if not project_root.is_dir():
        raise SystemExit(f"Project path '{project_root}' is not a directory.")

    app = args.app_name or detect_app_name(project_root)
    app_root = project_root / app
    if not app_root.is_dir():
        raise SystemExit(
            f"App folder '{app}' not found at {app_root}. "
            "Pass --app-name with the correct folder name."
        )

    structured_stencil = (STENCILS_DIR / "custom-structured-swift5.stencil").read_text(encoding="utf-8")
    assets_stencil = (STENCILS_DIR / "custom-assets-swiftui.stencil").read_text(encoding="utf-8")

    print()
    print(f"Project root: {project_root}")
    print(f"App name:     {app}")
    if args.dry_run:
        print("Mode:         DRY RUN — no files will be modified")

    print("\nSwiftGen support files:")
    print(write_file(
        "SwiftGen/Scripts/custom-structured-swift5.stencil",
        structured_stencil,
        project_root,
        args.force,
        dry_run=args.dry_run,
    ))
    print(write_file(
        "SwiftGen/Templates/custom-assets-swiftui.stencil",
        assets_stencil,
        project_root,
        args.force,
        dry_run=args.dry_run,
    ))
    print(write_file(
        "swiftgen.yml",
        SWIFTGEN_YML_TEMPLATE.format(app=app),
        project_root,
        args.force,
        dry_run=args.dry_run,
    ))

    print("\nApp-side folders SwiftGen reads/writes:")
    print(ensure_dir(f"{app}/Assets", project_root, dry_run=args.dry_run))
    print(ensure_dir(f"{app}/Assets/Localization", project_root, dry_run=args.dry_run))
    print(ensure_dir(f"{app}/Supporting files/en.lproj", project_root, dry_run=args.dry_run))
    print(ensure_dir(f"{app}/Supporting files/Assets.xcassets", project_root, dry_run=args.dry_run))

    print("\nPlaceholder inputs (only if missing):")
    print(write_file(
        f"{app}/Supporting files/en.lproj/Localizable.strings",
        LOCALIZABLE_PLACEHOLDER,
        project_root,
        force=False,
        only_if_missing=True,
        dry_run=args.dry_run,
    ))
    print(write_file(
        f"{app}/Supporting files/Assets.xcassets/Contents.json",
        XCASSETS_CONTENTS_JSON,
        project_root,
        force=False,
        only_if_missing=True,
        dry_run=args.dry_run,
    ))

    if args.dry_run:
        print("\nDry run complete — no changes made. Re-run without --dry-run to apply.")
    else:
        print("\nDone. Next: run `swiftgen` from the project root.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
