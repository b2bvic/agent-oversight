# Build a macOS release

You need arm64 macOS, Python 3.11+, and the Xcode command line tools.

**v0.1.0** packaged a clang launcher that embedded the Bash `agent-monitor` script and exec'd `/bin/bash`. **0.2.0 (unreleased)** packages the Python 3.11+ entrypoint with a pinned PyInstaller onefile build. This pass updates the build script only; it does not install into live paths.

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
