#!/usr/bin/env python3
"""Build an arm64 macOS onefile binary from the Python entrypoint."""

import argparse
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import venv

# Pin PyInstaller to record the packaging tool version.
PYINSTALLER_VERSION = "6.22.2"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        parser.error("Build on arm64 macOS with the Xcode command line tools.")
    if sys.version_info < (3, 11):
        parser.error("Python 3.11+ is required to build agent-monitor 0.2.0.")
    root = Path(__file__).resolve().parent.parent
    script = root / "agent-monitor"
    if not script.is_file():
        parser.error(f"Missing entrypoint: {script}")
    output = args.output.resolve()
    if output.exists() and output.is_dir():
        parser.error("Output path is a directory.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="agent-monitor-build-") as tmp:
        tmp_path = Path(tmp)
        venv_dir = tmp_path / "venv"
        venv.create(venv_dir, with_pip=True)
        python = venv_dir / "bin" / "python"
        subprocess.run(
            [str(python), "-m", "pip", "install", f"pyinstaller=={PYINSTALLER_VERSION}"],
            check=True,
        )
        # PyInstaller expects a .py suffix; copy without touching the live entrypoint name.
        source = tmp_path / "agent_monitor.py"
        source.write_bytes(script.read_bytes())
        dist = tmp_path / "dist"
        work = tmp_path / "work"
        specdir = tmp_path / "spec"
        subprocess.run(
            [
                str(python),
                "-m",
                "PyInstaller",
                "--onefile",
                "--clean",
                "--noconfirm",
                "--name",
                output.name,
                "--distpath",
                str(dist),
                "--workpath",
                str(work),
                "--specpath",
                str(specdir),
                str(source),
            ],
            check=True,
        )
        built = dist / output.name
        os.replace(built, output)
        subprocess.run(
            ["codesign", "--force", "--sign", "-", str(output)],
            check=True,
        )
    print(output)


if __name__ == "__main__":
    main()
