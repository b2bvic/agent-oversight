#!/usr/bin/env python3
"""Build an arm64 macOS launcher with the current Bash script embedded."""

import argparse
from pathlib import Path
import platform
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        parser.error("Build on arm64 macOS with the Xcode command line tools.")
    root = Path(__file__).resolve().parent.parent
    script = (root / "agent-monitor").read_bytes()
    if b"\0" in script:
        parser.error("The Bash source contains a NUL byte.")
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = ",".join(str(byte) for byte in script + b"\0")
    source = """#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
static char script[] = {PAYLOAD};
int main(int argc, char **argv) {
    char **args = calloc((size_t)argc + 4, sizeof(char *));
    if (!args) { perror("calloc"); return 1; }
    args[0] = "/bin/bash";
    args[1] = "-c";
    args[2] = script;
    args[3] = "agent-monitor";
    for (int i = 1; i < argc; ++i) args[i + 3] = argv[i];
    execv(args[0], args);
    perror("execv /bin/bash");
    free(args);
    return 126;
}
""".replace("PAYLOAD", payload)
    with tempfile.TemporaryDirectory(dir=output.parent) as temp:
        c_file = Path(temp) / "launcher.c"
        c_file.write_text(source)
        subprocess.run([
            "clang", "-arch", "arm64", "-mmacosx-version-min=11.0",
            "-Os", "-Wall", "-Wextra", "-Werror", str(c_file), "-o", str(output),
        ], check=True)
    print(output)


if __name__ == "__main__":
    main()
