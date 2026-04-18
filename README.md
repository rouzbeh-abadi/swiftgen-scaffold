# swiftgen-scaffold

> Interactive Python scaffolder that drops SwiftGen config, stencils, and required folders into any iOS project.

A small, dependency-free Python tool that bootstraps everything [SwiftGen](https://github.com/SwiftGen/SwiftGen) needs in an iOS Xcode project: the `swiftgen.yml` config, custom stencil templates for SwiftUI assets and structured strings, and the input/output folders inside the app target. Run the script, paste your project path when prompted, and you're ready to `swiftgen`.

---

## Project structure

```
swiftgen-scaffold/
├── swiftgen_scaffold.py            ← run this
├── lib/
│   ├── __init__.py
│   ├── detector.py                 ← detects app name from .xcodeproj
│   ├── writer.py                   ← write-file / ensure-dir helpers
│   └── templates.py                ← swiftgen.yml + small placeholders
├── stencils/
│   ├── custom-structured-swift5.stencil   ← Localizable.strings → L10n
│   └── custom-assets-swiftui.stencil      ← Assets.xcassets → Asset (SwiftUI)
├── README.md
├── LICENSE
└── .gitignore
```

| File / folder | Role | You run it? |
| --- | --- | --- |
| [`swiftgen_scaffold.py`](swiftgen_scaffold.py) | **Entry point.** Prompts for the project path, orchestrates the scaffold, prints the action log. | **Yes — this is the only file you invoke.** |
| [`lib/detector.py`](lib/detector.py) | Auto-detects your app folder name from `.xcodeproj` / `.xcworkspace`. | No. |
| [`lib/writer.py`](lib/writer.py) | Filesystem helpers: write-file-if-missing, ensure-dir, dry-run support. | No. |
| [`lib/templates.py`](lib/templates.py) | The `swiftgen.yml` template plus tiny placeholders for `Localizable.strings` and `Assets.xcassets/Contents.json`. | No. |
| [`stencils/`](stencils) | The two SwiftGen stencils as plain `.stencil` files — copied verbatim into your project. Edit them as plain text. | No. |

`swiftgen_scaffold.py` is the only file you invoke. It imports `lib/` by name and reads `stencils/` by relative path, so all three (entry point, `lib/`, `stencils/`) must sit side-by-side.

---

## Requirements

- Python 3.8+
- An Xcode project (`.xcodeproj` or `.xcworkspace`) inside the project path you paste in
- [SwiftGen](https://github.com/SwiftGen/SwiftGen) installed separately (e.g. `brew install swiftgen`) — this tool only generates the configuration

---

## Usage

The scaffolder is interactive. **You only need to do three things: get your project path, run the script, paste the path.**

### Step 1 — Get your iOS project's path

Open Terminal in your iOS project and copy the absolute path:

```bash
cd /Users/me/Projects/MyApp
pwd
# /Users/me/Projects/MyApp     ← copy this line
```

### Step 2 — Run the scaffolder

From the same Terminal (or any other), run:

```bash
python3 ~/tools/swiftgen-scaffold/swiftgen_scaffold.py
```

Replace `~/tools/swiftgen-scaffold/` with wherever you cloned this repo.

### Step 3 — Paste your project path at the prompt

```
Tip: in your iOS project's Terminal, run `pwd` and copy the path.
Press Enter to use the current directory.

Project path: /Users/me/Projects/MyApp     ← paste here, then hit Enter
```

That's it. The scaffolder reads your project path, detects the app folder from the `.xcodeproj`, and writes everything in place.

> **Shortcut**: if you're already `cd`'d into the iOS project, just press Enter at the prompt — the current directory is used.

### Run it directly (optional)

The script ships with a `#!/usr/bin/env python3` shebang and the executable bit set, so you can invoke it without typing `python3`:

```bash
~/tools/swiftgen-scaffold/swiftgen_scaffold.py
```

For an even shorter command, symlink it onto your `PATH`:

```bash
ln -s ~/tools/swiftgen-scaffold/swiftgen_scaffold.py /usr/local/bin/swiftgen-scaffold
swiftgen-scaffold
```

### Optional flags

| Flag | Description |
| --- | --- |
| `--app-name NAME` | Override the auto-detected app folder name (when it differs from the `.xcodeproj` stem, or when there are multiple projects). |
| `--force` | Overwrite an existing `swiftgen.yml` and the two stencil templates. App-side files (`Localizable.strings`, `Contents.json`) are never overwritten. |
| `--dry-run` | Preview every action — show exactly what would be written and which folders would be created — without touching disk. Combine with the path prompt to test against a real project safely. |

```bash
# See what would happen, without writing anything
python3 ~/tools/swiftgen-scaffold/swiftgen_scaffold.py --dry-run

# Override the detected app name
python3 ~/tools/swiftgen-scaffold/swiftgen_scaffold.py --app-name MyApp

# Re-sync stencils and yml after upstream tweaks
python3 ~/tools/swiftgen-scaffold/swiftgen_scaffold.py --force
```

The path prompt still appears with these flags — paste your project path as usual.

---

## What it creates

Given a project named `MyApp`, the script produces:

```
MyApp/                                         (your project root)
├── swiftgen.yml                               ← config (paths bound to MyApp)
├── SwiftGen/
│   ├── Scripts/
│   │   └── custom-structured-swift5.stencil   ← Localizable.strings → L10n enum
│   └── Templates/
│       └── custom-assets-swiftui.stencil      ← Assets.xcassets → Asset enum (SwiftUI)
└── MyApp/
    ├── Assets/                                ← OUTPUT: Assets-Constants.swift lands here
    │   └── Localization/                      ← OUTPUT: L10n-Constants.swift lands here
    └── Supporting files/
        ├── en.lproj/
        │   └── Localizable.strings            ← INPUT (placeholder created if missing)
        └── Assets.xcassets/
            └── Contents.json                  ← INPUT (placeholder created if missing)
```

After running, execute `swiftgen` from the project root and the generated Swift files will appear in `MyApp/Assets/` and `MyApp/Assets/Localization/`. Add those files to your Xcode target.

---

## Adding a new language

If you later create a new language folder yourself (e.g. `de.lproj/Localizable.strings`), there's one Xcode step the scaffolder cannot do for you:

- **Xcode will display the file** in the navigator and **bundle it** into the `.app`.
- **The OS will not actually serve the German strings at runtime** until you register German as a supported language — this lives inside `project.pbxproj`'s `knownRegions` / the app's `CFBundleLocalizations`, not in the file system.

Register the language **once** via *Project → Info → Localizations → +*. After that, every subsequent edit to `de.lproj/Localizable.strings` works without any further Xcode action.

This caveat is the same regardless of how the file gets created — it's an Xcode requirement, not a limitation of this scaffolder.

---

## The two stencils

Both templates are tuned for modern SwiftUI iOS projects.

### `stencils/custom-assets-swiftui.stencil`

Generates a SwiftUI-friendly `Asset` enum from your `Assets.xcassets`:

- `Asset.someImage.image` returns a SwiftUI `Image`
- `Asset.someColor.color` returns a SwiftUI `Color`
- `Image(Asset.someImage)` and `Color(Asset.someColor)` initializers are also provided
- All types are `Sendable` for Swift Concurrency

### `stencils/custom-structured-swift5.stencil`

Generates a nested `L10n` enum from your `Localizable.strings`:

- `L10n.someKey` for plain strings
- `L10n.welcome("Alice")` for strings with format arguments
- Comments are preserved as `///` doc comments
- Bundle resolution works in both apps and Swift packages

---

## Behavior on re-runs

The script is safe to run repeatedly:

- **Folders** are created if missing, left alone if they exist.
- **`swiftgen.yml` and stencils** are skipped if they already exist. Pass `--force` to overwrite.
- **Placeholder `Localizable.strings` and `Contents.json`** are only written when missing — your real content is never touched.
- **`--dry-run`** never writes anything, regardless of any other flag.

---

## Auto-detection

The script picks the app name in this order:

1. The value passed via `--app-name`.
2. The stem of the single `.xcodeproj` in the project path you pasted.
3. The stem of the single `.xcworkspace` if no `.xcodeproj` is found.

If multiple `.xcodeproj` files are present, it errors out and asks you to specify `--app-name`.

The detected name is also assumed to be the **app folder name** (the folder Xcode creates for your app target's sources). If your folder name differs from the project name, pass `--app-name` with the folder name.

---

## Customizing what gets generated

Two places to edit, depending on what you want to change:

| Want to change | Edit | Notes |
| --- | --- | --- |
| The generated Swift code shape (asset enum, L10n enum) | [`stencils/custom-assets-swiftui.stencil`](stencils/custom-assets-swiftui.stencil) or [`stencils/custom-structured-swift5.stencil`](stencils/custom-structured-swift5.stencil) | Plain SwiftGen stencil files — edit as text, no Python escaping. |
| The `swiftgen.yml` layout, paths, or params | `SWIFTGEN_YML_TEMPLATE` in [`lib/templates.py`](lib/templates.py) | The `{app}` placeholder is substituted at runtime. |
| The placeholder `Localizable.strings` or `Contents.json` content | `LOCALIZABLE_PLACEHOLDER` / `XCASSETS_CONTENTS_JSON` in [`lib/templates.py`](lib/templates.py) | Only written when the target file doesn't already exist. |

For per-project tweaks instead of global ones, run the scaffolder once and then edit the generated stencil/yml files directly inside the project — future runs without `--force` won't touch your edits.

---

## License

MIT — see [LICENSE](LICENSE).
