# Build a macOS release

You need arm64 macOS, Python 3, and the Xcode command line tools.
Run this command from the repository root:

```bash
python3 scripts/build-macos.py --output .git/release/agent-monitor-macos-arm64
```

The binary embeds the current `agent-monitor` script and passes your arguments to `/bin/bash`.
You still need macOS shell utilities at runtime. You do not need Python to run the binary.
The launcher preserves the script's process matching and session counting behavior.

Verify the architecture and signature:

```bash
file .git/release/agent-monitor-macos-arm64
codesign --verify .git/release/agent-monitor-macos-arm64
```

The build uses an ad hoc signature. You do not get an Apple notarization ticket.
