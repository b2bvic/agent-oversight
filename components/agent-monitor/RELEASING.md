# Build a macOS release

You need arm64 macOS, Python 3.11+, and the Xcode command line tools.

Version 0.1.0 embeds the Bash script in a native launcher.
Version 0.2.0 bundles the Python entrypoint with PyInstaller.
Use the matching release tag when you reproduce a published build.

Run this command from the repository root:

```bash
python3 scripts/build-macos.py --output .git/release/agent-monitor-macos-arm64
```

The script creates a temporary virtualenv, installs `pyinstaller==6.22.2`, and writes the binary to `--output`. It does not copy the result to `~/.local/bin` or otherwise activate it. You do not need Python to run the binary after it is built.

Verify the architecture and signature:

```bash
file .git/release/agent-monitor-macos-arm64
codesign --verify .git/release/agent-monitor-macos-arm64
```

The build uses an ad hoc signature. You do not get an Apple notarization ticket.
